'''
TPO-COM Database helper functions
'''
import pyodbc

def get_db_name(point):
    '''
    Returns the database name by looking into the first three letters
    in the point name.
    '''
    return point['name'][0:3]

def get_tracker_db():
    '''
    Returns the database name for the tracker tables.
    '''
    return 'TPOCOM'

def get_input_table_name(point):
    '''
    Returns the table name for the input point by combining point name
    sig_code and sig_prog
    '''
    return (point['name'][0:3] 
            + '---------' # ZONE, QUADRANT, FLOOR
            + point['name'][12:-3] 
            + '---' # EQUIPMENT NUMBER
            + point['sig_code'] + point['sig_prog'])

def get_output_table_name(point):
    '''
    Returns the table name for the output point by combining point name,
    sig_code
    '''
    return (point['name'][0:3] 
            + '---------' # ZONE, QUADRANT, FLOOR
            + point['name'][12:] 
            + '---' # SIG CODE
            + point['sig_prog'])


def get_tracker_table_name(point):
    '''
    Returns the name for the tracker table.
    '''
    return get_output_table_name(point) + '_sendid_tracker'

def get_input_point_val_type(point):
    '''
    Return the database data type for the point based on the SIF point type
    '''
    value_type_dict = {'measure':'float','status':'float','alarm':'varchar'}
    return value_type_dict[point['point_type']]

def create_tpocom_input_tables(db_server, points):
    '''
    Creates database db and input tables for every point in 'points'
    '''
    create_database(db_server, get_db_name(points[0]))
    for point in points:
        create_input_table(db_server, get_db_name(point),
                             get_input_table_name(point),
                             get_input_point_val_type(point))

def create_tpocom_output_tables(db_server, points):
    '''
    Creates database db and output tables for all the points.
    '''
    create_database(db_server, get_db_name(points[0]))
    for point in points:
        create_output_table(db_server, get_db_name(point),
                             get_output_table_name(point),
                             point['point_type'])
        
def create_tracker_tables(db_server, points):
    '''
    creates database db and tables to track points sent to SIF.
    '''
    create_database(db_server, get_tracker_db())
    for point in points:
        create_tracker_table(db_server, get_tracker_db(),
                             get_tracker_table_name(point))

def create_connection(db_server):
    '''
    Creates connection to the database server db_server and returns
    the connection object
    '''
    conn_string = ('DRIVER={SQL Server}'
                    +';SERVER='+db_server['SERVER']
                    +';UID='+db_server['UID']
                    +';PWD='+db_server['PWD'])
    return pyodbc.connect(conn_string)

    
def create_database(db_server, db):
    '''
    Creates a new database db if it does not already exist 
    at the db_server. db_server is a dictionary of this form:
    {'SERVER':'server.edu','UID':'user','PWD':'psswd'}
    '''
    conn = create_connection(db_server)
    conn.autocommit = True
    cursor = conn.cursor()
    cmd = ('IF NOT EXISTS '
                    +'(SELECT name FROM master.dbo.sysdatabases WHERE name = \'' 
                    + db+'\')'
                    + 'CREATE DATABASE [' + db + ']')
    cursor.execute(cmd)
    conn.autocommit = False
    
def create_input_table(db_server, db, db_table, value_dtype):
    '''
    Creates a new table db_table in database db if it does 
    not already exist. db_server is a dictionary of this form:
    {'SERVER':'server.edu','UID':'user','PWD':'psswd'}
    '''
    conn = create_connection(db_server)
    cursor = conn.cursor()
    cmd = ('IF NOT EXISTS '
                    +'(SELECT name FROM [' + db + '].sys.tables WHERE name = \'' 
                    + db_table + '\') '
                    + 'CREATE TABLE [' + db + '].[dbo].[' + db_table + ']'
                    + '( ID int IDENTITY(1,1) PRIMARY KEY, ZONE nchar(3),'
                    + 'FLOOR nchar(3), QUADRANT nchar(3), EQUIPMENT_NO nchar(3),'
                    + 'TIMESTAMP datetime, VALUE ' + value_dtype +')')
    cursor.execute(cmd)  
    conn.commit()
    
    
def create_output_table(db_server, db, db_table, point_type):
    '''
    Creates a new output table db_table in database db if it does 
    not already exist. The columns in the table are determined by the point_type.
    db_server is a dictionary of this form:
    {'SERVER':'server.edu','UID':'user','PWD':'psswd'}
    '''    
    conn = create_connection(db_server)
    cursor = conn.cursor()
    crt_table_cmd = ''
    if point_type == 'measure':
        primary_id_cols = ('[Run_DateTime] [datetime] NOT NULL,'
                            +'[Prediction_DateTime] [datetime] NOT NULL,')
        non_primary_id_cols = ('[Floor] [nvarchar](20) NULL,'
                            +'[Quadrant] [nvarchar](20) NULL,')
        primary_key_constraints = ('PRIMARY KEY CLUSTERED ('
                                    +'[Run_DateTime] ASC,'
                                    +'[Prediction_DateTime] ASC)')
        # for space temperature add floor and quadrant in the primary key cluster
        if db_table[18:24] in set(['FORTEM','HVATEM']):
            primary_id_cols = ('[Run_DateTime] [datetime] NOT NULL,'
                            +'[Prediction_DateTime] [datetime] NOT NULL,'
                            +'[Floor] [nvarchar](20) NOT NULL,'
                            +'[Quadrant] [nvarchar](20) NOT NULL,')
            non_primary_id_cols = ''
            primary_key_constraints = ('PRIMARY KEY CLUSTERED ('
                                    +'[Run_DateTime] ASC,'
                                    +'[Floor] ASC,'
                                    +'[Quadrant] ASC,'
                                    +'[Prediction_DateTime] ASC)')            
                                    
        crt_table_cmd = ('CREATE TABLE ['+ db +'].[dbo].['+ db_table +']('
                + primary_id_cols
                + non_primary_id_cols
                +'[Zone] [nvarchar](20) NULL,'
                +'[Prediction_Value] [float] NULL,'
                +'[Lower_Bound_95] [float] NULL,'
                +'[Upper_Bound_95] [float] NULL,'
                +'[Lower_Bound_68] [float] NULL,'
                +'[Upper_Bound_68] [float] NULL,'
                +'[ID] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,'
                + primary_key_constraints
                +'WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF,'
                +'IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON,'
                +'ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY])'
                +'ON [PRIMARY]')
    elif point_type == 'status':
        crt_table_cmd = ('CREATE TABLE ['+ db +'].[dbo].['+ db_table +']('
                +'[ID] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,'
                +'[Run_DateTime] [datetime] NULL,'
                +'[Prediction_DateTime] [datetime] NULL,'
                +'PRIMARY KEY CLUSTERED ('
                +'[ID] ASC) '
                +'WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF,' 
                +'IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON,'
                +'ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY])'
                +'ON [PRIMARY]')
    elif point_type == 'alarm':
        crt_table_cmd = ('CREATE TABLE ['+ db +'].[dbo].['+ db_table +']('
                +'[ID] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,'
                +'[STATE] [int] NULL,'
                +'[PROPERTY_PRIO] [int] NULL,'
                +'[INTERNAL] [int] NULL,'
                +'[INITTS] [datetime] NULL,'
                +'[NORMTS] [datetime] NULL,'
                +'[PBS] [varchar](10) NULL,'
                +'[SIGN] [varchar](100) NULL,'
                +'[Sign_Prog] [char](3) NOT NULL,'
                +'PRIMARY KEY CLUSTERED ('
                +'[ID] ASC )'
                +'WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF,' 
                +'IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON,' 
                +'ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY])'
                +'ON [PRIMARY]')
    else: 
        print 'point type '+point_type+' not supported'
        return
    
    cmd = ('IF NOT EXISTS '
                    +'(SELECT name FROM [' + db + '].sys.tables WHERE name = \'' 
                    + db_table + '\') '
                    + crt_table_cmd)
    cursor.execute(cmd)  
    conn.commit()   

def create_tracker_table(db_server, db, db_table):
    '''
    Creates a new tracker table db_table in database db if it does 
    not already exist. Also initializes the table with one entry '0'.
    db_server is a dictionary of this form:
    {'SERVER':'server.edu','UID':'user','PWD':'psswd'}
    '''
    conn = create_connection(db_server)
    cursor = conn.cursor()
    cmd = ('IF NOT EXISTS '
                    +'(SELECT name FROM [' + db + '].sys.tables WHERE name = \'' 
                    + db_table + '\') '
                    +'CREATE TABLE [' + db + '].[dbo].[' + db_table + ']'
                    +'(SENTID int); '
                    +'INSERT INTO [' + db + '].[dbo].[' + db_table + ']' + 'VALUES(0)')
    cursor.execute(cmd)  
    conn.commit()   
