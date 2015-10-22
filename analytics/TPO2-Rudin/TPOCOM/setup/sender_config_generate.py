'''
Main sender configuration generator
'''
import sys
import argparse
from workbook_helper import *
from sender_config_helper import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description =
                                        'Creates config file for TPO-COM sender.'
                                        'Lets you create a new config file or add '
                                        'a new building to the existing config file')
    parser.add_argument('workbook',help='path to pointlist workbook')
    parser.add_argument('server', help='database server address for tracking tables')
    parser.add_argument('uid', help='database server user id')
    parser.add_argument('pwd', help='database server user password')
    parser.add_argument('sif_server', help='sif endpoint address')
    parser.add_argument('sif_port', help='sif endpoint port')
    parser.add_argument('tpocom_server', help='tpo endpoint address for sif')
    parser.add_argument('tpocom_port', help='tpo endpoint port for sif')
    parser.add_argument('tpo_sender', help='tpo sender id')
    parser.add_argument('tpo_location_id', help='tpo location id')
    parser.add_argument('tpo_poll_int', help='tpo db poll interval in seconds')
    parser.add_argument('tpocom_version', help='tpocom version')
    parser.add_argument('timeout', help='timeout for sif tpocom connection in milli seconds')
    parser.add_argument('heart_beat_int', help='keep alive message interval in seconds')
    parser.add_argument('config', help='path to the config file')
    parser.add_argument('--overwrite', action='store_true', help=
                        'overwrite the config file if it exists. defaults to false and '
                        'adds the config for points to the given config file')
    
    args = parser.parse_args()
    db_server = {'SERVER':args.server, 'UID':args.uid, 'PWD':args.pwd}
    input_sheets = get_sheets(args.workbook, sheet_name_substr='TPO-output') 
    points = get_points(input_sheets)
    tpocom_settings = {'tpo_sender_id':args.tpo_sender,
                        'tpo_location_id':args.tpo_location_id,
                        'tpo_db_poll_interval_seconds':args.tpo_poll_int,
                        'tpocom_version':args.tpocom_version,
                        'tpocom_ttl_ms':args.timeout,
                        'tpocom_heart_beat_interval_sec':args.heart_beat_int}
    sif_endpoint = {'host':args.sif_server, 
                        'port':args.sif_port, 'path':'axis2/services/WSSB2'}
    tpo_endpoint = {'host':args.tpocom_server, 
                        'port':args.tpocom_port, 'path':'axis2/services/WSSB2'}                     
                        
    if args.overwrite:
        generate_sender_config(db_server, points, tpocom_settings,
                                    sif_endpoint, tpo_endpoint, args.config)
    else:
        extend_sender_config(db_server, points, tpocom_settings,
                                    sif_endpoint, tpo_endpoint, args.config)