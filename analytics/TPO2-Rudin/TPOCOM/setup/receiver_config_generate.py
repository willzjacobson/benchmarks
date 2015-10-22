'''
Main receiver configuration generator
'''
import sys
import argparse
from workbook_helper import get_sheets, get_points
from receiver_config_helper import extend_receiver_config, generate_receiver_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description =
                                        'Creates config file for TPO-COM receiver.'
                                        'Lets you create a new config file or add '
                                        'a new building to the existing config file')
    parser.add_argument('workbook',help='path to pointlist workbook')
    parser.add_argument('server', help='database server address')
    parser.add_argument('uid', help='database user id')
    parser.add_argument('pwd', help='database user password')
    parser.add_argument('config', help='path to the config file')
    parser.add_argument('--overwrite', action='store_true', help=
                        'overwrite the config file if it exists. defaults to false and '
                        'adds the config for points to the given config file')
    
    args = parser.parse_args()
    db_server = {'SERVER':args.server, 'UID':args.uid, 'PWD':args.pwd}
    input_sheets = get_sheets(args.workbook, sheet_name_substr='TPO-input') 
    points = get_points(input_sheets)
    if args.overwrite:
        generate_receiver_config(db_server, points, args.config)
    else:
        extend_receiver_config(db_server, points, args.config)