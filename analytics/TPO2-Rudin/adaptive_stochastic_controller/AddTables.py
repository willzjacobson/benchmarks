
import sys
import pyodbc
import ConfigParser

script = open('AddTables.txt', 'r')

query = ''
while True: 	
	line = script.read()
	if line == '':
		break
	query += line


#the master config file should be explicitly given along with the building section 
#for which the tables have to be created
#while calling the script
#for instance:
#>> python .\AddTables.py .\config.ini Rudin_345Park
#config_file = sys.argv[1]
config_file = '../config.ini'
section = sys.argv[1]

cparser = ConfigParser.ConfigParser()
cparser.readfp(open(config_file))	

tpo_server = cparser.get(section, 'results_db_server')
tpo_database = cparser.get(section, 'results_db')
tpo_user = cparser.get(section, 'results_db_user')
tpo_pwd = cparser.get(section, 'results_db_pwd')

connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(tpo_server, tpo_database, tpo_user, tpo_pwd)) 

cursor = connection.cursor()

for g in ['electric', 'temp', 'occupancy', 'steam', 'vfd', 'fan', 'sec', 'pump']:
	table_name = cparser.get(section, 'asc_output_'+g+'_table')
	query.format(tpo_database, table_name, table_name)
	cursor.execute(query)
cursor.commit()

cursor.close()
connection.close()
