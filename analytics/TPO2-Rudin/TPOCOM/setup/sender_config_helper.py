'''
Sender configuration helper module.
'''
import xml.etree.ElementTree as ET
from xml.dom import minidom
from db_helper import *

def create_tpocom_setting_nodes(top_node, tpocom_settings):
    '''
    Create and add tpocom_setting nodes to the top_node.
    '''
    ET.SubElement(top_node,'tpo_sender_id').text = tpocom_settings['tpo_sender_id']
    ET.SubElement(top_node,'tpo_location_id').text = tpocom_settings['tpo_location_id']
    ET.SubElement(top_node,'tpo_db_poll_interval_seconds').text = tpocom_settings['tpo_db_poll_interval_seconds']
    ET.SubElement(top_node,'tpocom_version').text = tpocom_settings['tpocom_version']
    ET.SubElement(top_node,'tpocom_ttl_ms').text = tpocom_settings['tpocom_ttl_ms']
    ET.SubElement(top_node,'tpocom_heart_beat_interval_sec').text = tpocom_settings['tpocom_heart_beat_interval_sec']
    
def create_sif_endpoint_node(top_node, sif_endpoint):
    '''
    Create and add sif_endpoint node to the top_node.
    '''
    sif_endpoint_node = ET.SubElement(top_node, 'sif_endpoint')
    ET.SubElement(sif_endpoint_node,'host').text = sif_endpoint['host']
    ET.SubElement(sif_endpoint_node,'port').text = sif_endpoint['port']
    ET.SubElement(sif_endpoint_node,'path').text = sif_endpoint['path']
    
def create_tpo_endpoint_node(top_node, tpo_endpoint):
    '''
    Create and add tpo_endpoint node to the top_node.
    '''
    tpo_endpoint_node = ET.SubElement(top_node, 'tpo_receiver_endpoint')
    ET.SubElement(tpo_endpoint_node,'host').text = tpo_endpoint['host']
    ET.SubElement(tpo_endpoint_node,'port').text = tpo_endpoint['port']
    ET.SubElement(tpo_endpoint_node,'path').text = tpo_endpoint['path']

def create_tpocom_subscription_node(top_node): 
    '''
    Create and add tpocom subscription nodes to the top_node: Subscribe for measure
    and status points.
    '''
    tpocom_subscription_node = ET.SubElement(top_node,'tpocom_subscription')
    subscription = ET.SubElement(tpocom_subscription_node, 'point',{'type':'measure'})
    ET.SubElement(subscription, 'subscription_name').text = 'measure.>'
    ET.SubElement(subscription, 'filter').text = 'measure/sender'
    subscription = ET.SubElement(tpocom_subscription_node, 'point',{'type':'status'})
    ET.SubElement(subscription, 'subscription_name').text = 'status.>'
    ET.SubElement(subscription, 'filter').text = 'status/sender'
    
def get_db_config_node(db_server, point):
    '''
    Returns db_config node for the given point.
    '''
    dbc_root = ET.Element("database_config", {"name":get_output_table_name(point)}) 
    ET.SubElement(dbc_root, "host").text = db_server['SERVER']
    ET.SubElement(dbc_root, "port").text = '1433'
    ET.SubElement(dbc_root, "database").text = get_db_name(point)
    ET.SubElement(dbc_root, "table").text = "dbo.["+get_output_table_name(point)+"]"
    ET.SubElement(dbc_root, "user").text = db_server['UID']
    ET.SubElement(dbc_root, "password").text = db_server['PWD']
    return dbc_root

def get_tracker_db_config_node(db_server, point):
    '''
    Returns the tracker_db_config node for the given point.
    '''
    dbc_root = ET.Element("database_config", {"name":get_tracker_table_name(point)}) 
    ET.SubElement(dbc_root, "host").text = db_server['SERVER']
    ET.SubElement(dbc_root, "port").text = '1433'
    ET.SubElement(dbc_root, "database").text = get_tracker_db()
    ET.SubElement(dbc_root, "table").text = "dbo.["+get_tracker_table_name(point)+"]"
    ET.SubElement(dbc_root, "user").text = db_server['UID']
    ET.SubElement(dbc_root, "password").text = db_server['PWD']
    return dbc_root

def get_point_config_node(point):
    '''
    Returns the point config node for the given point
    '''
    pt_config = ET.Element('point_config', {'name':get_output_table_name(point)})
    ET.SubElement(pt_config, 'database').text = get_output_table_name(point)
    ET.SubElement(pt_config, 'send_tracker_database').text = get_tracker_table_name(point)
    ET.SubElement(pt_config, 'primary_column').text='ID'
    ET.SubElement(pt_config, 'tracker_column').text='SENTID'
    
    pt_constants = ET.SubElement(pt_config, 'point_constants')
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Loc_A1'}).text = point['name'][0:3]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Sys_T'}).text = point['name'][12:15]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Sys_S'}).text = point['name'][15:18]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Eq_L1'}).text = point['name'][18:21]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Eq_L2'}).text = point['name'][21:24]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Eq_L3'}).text = point['name'][24:27]
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Eq_n'}).text = point['name'][27:30]
    ET.SubElement(pt_constants,'constant',{'pointName':'Sign_Prog'}).text = point['sig_prog']
    ET.SubElement(pt_constants,'constant',{'pointName':'Sender'}).text = point['name'][12:15]+point['name'][15:18]
    ET.SubElement(pt_constants,'constant',{'pointName':'Realtime'}).text = '1'
    ET.SubElement(pt_constants,'constant',{'pointName':'Pbs_Native'}).text = point['name']
    ET.SubElement(pt_constants,'constant',{'pointName':'Point_Type'}).text = point['point_type']
    
    # set the value code to db column maps
    if point['name'][18:24] == 'OPTTEM' :
        # Recommendations only
        vc_map = ET.SubElement(pt_config, 'value_codes_AND_column_maps')
        ET.SubElement(vc_map, 'constant',{'colName':'Prediction_DateTime', 'valueDataType':'string'}).text='VAL'
    
    elif point['name'][18:24] in set(['FORTEM','FORELE','FORSTE','FORPEO','HVATEM']):
        #Forecasting only
        vc_map = ET.SubElement(pt_config, 'value_codes_AND_column_maps')
        ET.SubElement(vc_map, 'constant',{'colName':'Prediction_Value', 'valueDataType':'double'}).text='VAL'
        ET.SubElement(vc_map, 'constant',{'colName':'Lower_Bound_95', 'valueDataType':'double'}).text='VLOLIM'
        ET.SubElement(vc_map, 'constant',{'colName':'Upper_Bound_95', 'valueDataType':'double'}).text='VHILIM'
        ET.SubElement(vc_map, 'constant',{'colName':'Lower_Bound_68', 'valueDataType':'double'}).text='LOLIM'
        ET.SubElement(vc_map, 'constant',{'colName':'Upper_Bound_68', 'valueDataType':'double'}).text='HILIM'
    
    # set the variables that are to be read from tables.
    if point['name'][18:24] == 'OPTTEM' :
        # Recommendations only   
        pt_variables = ET.SubElement(pt_config, 'point_variables')
        ET.SubElement(pt_variables, 'variable',{'colName':'Prediction_DateTime', 'pointDataType':'date'}).text='RefTs'

    elif point['name'][18:24] in set(['FORTEM','HVATEM']):
        # Space temperature points read zone and floor from a single table
        pt_variables = ET.SubElement(pt_config, 'point_variables')
        ET.SubElement(pt_variables, 'variable',{'colName':'ZONE', 'pointDataType':'string'}).text='Pbs_Loc_A2'
        ET.SubElement(pt_variables, 'variable',{'colName':'Floor', 'pointDataType':'string'}).text='Pbs_Loc_A3'
        ET.SubElement(pt_variables, 'variable',{'colName':'Quadrant', 'pointDataType':'string'}).text='Pbs_Loc_A4'
    else:
        pt_variables = ET.SubElement(pt_config, 'point_variables')
        ET.SubElement(pt_config, 'point_variables')
        
    # set the value attributes
    if point['name'][18:24] in set(['OPTTEM']):
        ET.SubElement(pt_config, 'value_attributes')
    else:
        val_attr_node = ET.SubElement(pt_config, 'value_attributes')
        ET.SubElement(pt_variables,  'variable',{'colName':'Prediction_DateTime', 'pointDataType':'date'}).text='RefTs'
    return pt_config

def get_sender_config_nodes(db_server, points):
    '''
    Returns all the databases, tracker databases and config nodes for the points.
    '''
    seen = set([])
    databases = []
    pnt_configs = []
    for point in points:
        point_name = get_output_table_name(point)
        if point_name in seen: continue
        seen.add(point_name)
        databases.append(get_db_config_node(db_server, point))
        databases.append(get_tracker_db_config_node(db_server, point))
        pnt_configs.append(get_point_config_node(point))
    return (databases, pnt_configs)
    
def generate_sender_config(db_server, points, tpocom_settings, sif_endpoint, tpo_endpoint, outfile):
    '''
    Generates a new sender configuration and writes the configuration file to the outfile.
    '''
    (databases, pnt_configs) = get_sender_config_nodes(db_server, points)
    top_node = ET.Element("tpocom_configuration")
    create_tpocom_setting_nodes(top_node, tpocom_settings)
    create_tpo_endpoint_node(top_node, tpo_endpoint)
    create_sif_endpoint_node(top_node, sif_endpoint)
    create_tpocom_subscription_node(top_node)
    databases_node = ET.SubElement(top_node, "databases")
    points_config_node = ET.SubElement(top_node, "points_config")
    for db_node in databases:
        databases_node.append(db_node)
    for pnt_node in pnt_configs: 
        points_config_node.append(pnt_node)
    xml_string = minidom.parseString(ET.tostring(top_node)).toprettyxml(indent="  ")
    with open(outfile, 'w') as outxml:
        outxml.write(xml_string)

def extend_sender_config(db_server, points, tpocom_settings, sif_endpoint, tpo_endpoint, old_xml):
    '''
    Extends the existing configuration file for the new points and writes it to the old_xml.
    '''
    try:
        ox = open(old_xml)
        tpocom_config_tree = ET.parse(ox)
        ox.close()
        tpocom_top_node = tpocom_config_tree.getroot()
        databases_node = tpocom_config_tree.find("databases")
        points_config_node = tpocom_config_tree.find("points_config")
        (databases, pnt_configs) = get_sender_config_nodes(db_server, points)    
        
        ## gather list of databases_node names and point_config_node names
        ## to make sure new node you are adding are not already there.
        db_node_names = set([db_node.attrib['name']for db_node in databases_node])
        point_config_names = set([pt_node.attrib['name']for pt_node in points_config_node])
        
        for db_node in databases: 
            if db_node.attrib['name'] not in db_node_names: databases_node.append(db_node)
        for pnt_node in pnt_configs: 
            if pnt_node.attrib['name'] not in point_config_names: points_config_node.append(pnt_node)
            
        xml_string = minidom.parseString(ET.tostring(tpocom_top_node)) \
            .toprettyxml()
        ## handling the extra lines printed by this prettyprint
        ##        dumbass library
        xml_string = '\n'.join([line for line in xml_string.split('\n')
                                                if line.strip()])
        with open(old_xml, 'w') as outxml:
            outxml.write(xml_string)    
    except:
        # if there is no valid xml fall back
        generate_sender_config(db_server, points, tpocom_settings, sif_endpoint, tpo_endpoint, old_xml)
        return