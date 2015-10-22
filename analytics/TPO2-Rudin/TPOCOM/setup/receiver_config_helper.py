'''
Receiver configuration helper module
'''
import xml.etree.ElementTree as ET
from xml.dom import minidom
from db_helper import *

def get_receiver_database_config(db_server, point):
    '''
    Returns db config node for the give point.
    '''
    dbc_root = ET.Element("database_config", {"name":get_input_table_name(point)}) 
    ET.SubElement(dbc_root, "host").text = db_server['SERVER']
    ET.SubElement(dbc_root, "port").text = '1433'
    ET.SubElement(dbc_root, "database").text = get_db_name(point)
    ET.SubElement(dbc_root, "table").text = "dbo.["+get_input_table_name(point)+"]"
    ET.SubElement(dbc_root, "user").text = db_server['UID']
    ET.SubElement(dbc_root, "password").text = db_server['PWD']
    return dbc_root

def get_receiver_point_config(point):
    '''
    Returns point config node for the given point.
    '''
    db_table = get_input_table_name(point)
    pnt_config_root = ET.Element("point_config",{"name":db_table});
    ET.SubElement(pnt_config_root,"database").text = db_table
    point_identifiers = ET.SubElement(pnt_config_root,"point_identifiers")
    id = "identifier"
    name = "name"
    ET.SubElement(point_identifiers, id, {name:"Pbs_Loc_A1"}).text = \
                                                    point['name'][0:3]
    ET.SubElement(point_identifiers, id, {name:"Pbs_Sys_T"}).text = \
                                                    point['name'][12:15]
    ET.SubElement(point_identifiers, id, {name:"Pbs_Sys_S"}).text = \
                                                    point['name'][15:18]
    ET.SubElement(point_identifiers, id, {name:"Pbs_Eq_L1"}).text = \
                                                    point['name'][18:21]
    ET.SubElement(point_identifiers, id, {name:"Pbs_Eq_L2"}).text = \
                                                    point['name'][21:24]
    ET.SubElement(point_identifiers, id, {name:"Pbs_Eq_L3"}).text = \
                                                    point['name'][24:27]
    ET.SubElement(point_identifiers, id, {name:"Sign_Code"}).text = \
                                                    point['sig_code']                                                    
    ET.SubElement(point_identifiers, id, {name:"Sign_Prog"}).text = \
                                                    point['sig_prog']            
    ET.SubElement(point_identifiers, id, {name:"Point_Type"}).text = \
                                                    point['point_type']    
    map = ET.SubElement(pnt_config_root,"point_column_map")
    ET.SubElement(map, "column", {name:"Pbs_Loc_A2"}).text = "ZONE"
    ET.SubElement(map, "column", {name:"Pbs_Loc_A3"}).text = "FLOOR"
    ET.SubElement(map, "column", {name:"Pbs_Loc_A4"}).text = "QUADRANT"
    ET.SubElement(map, "column", {name:"Pbs_Eq_n"}).text = "EQUIPMENT_NO"
    ET.SubElement(map, "column", {name:"Value"}).text = "VALUE"
    ET.SubElement(map, "column", {name:"ts"}).text = "TIMESTAMP"    
    return  pnt_config_root

def get_receiver_config_nodes(db_server, points):
    '''
    Return database config nodes and point config nodes for all the given points.
    '''        
    seen = set([])
    databases = []
    pnt_configs = []
    for point in points:
        point_name = get_input_table_name(point)
        if point_name in seen: continue
        seen.add(point_name)
        databases.append(get_receiver_database_config(db_server, point))
        pnt_configs.append(get_receiver_point_config(point))
    return (databases, pnt_configs)
    
def generate_receiver_config(db_server, points, outfile):
    '''
    Generates receiver configuration file and writes it to the outfile. 
    '''
    (databases, pnt_configs) = get_receiver_config_nodes(
                                        db_server, points)
    tpocom_top_node = ET.Element("tpocom_configuration")
    databases_node = ET.SubElement(tpocom_top_node, "databases")
    points_config_node = ET.SubElement(tpocom_top_node, "points_config")
    for db_node in databases: databases_node.append(db_node)
    for pnt_node in pnt_configs: points_config_node.append(pnt_node)
    xml_string = minidom.parseString(ET.tostring(tpocom_top_node)) \
                .toprettyxml(indent="  ")
    with open(outfile, 'w') as outxml:
        outxml.write(xml_string)
        
def extend_receiver_config(db_server, points, old_xml):
    '''
    Extends the existing configuration file and write it to the outfile.
    '''
    try:
        ox = open(old_xml)
        tpocom_config_tree = ET.parse(ox)
        ox.close()
        tpocom_top_node = tpocom_config_tree.getroot()
        databases_node = tpocom_config_tree.find("databases")
        points_config_node = tpocom_config_tree.find("points_config")
        (databases, pnt_configs) = get_receiver_config_nodes(
                                        db_server, points)    
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
        generate_receiver_config(db_server, points, old_xml)
        return