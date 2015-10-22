'''
Main for setting up TPO output databases.
'''
import sys
import argparse
from workbook_helper import get_sheets, get_points
from db_helper import create_tpocom_output_tables, create_tracker_tables

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description =
                                        'Creates database for tpo outputs '
                                        'for a new building.')
    parser.add_argument('workbook',help='path to pointlist workbook')
    parser.add_argument('server', help='database server address')
    parser.add_argument('uid', help='database user id')
    parser.add_argument('pwd', help='database user password')
    
    args = parser.parse_args()
    db_server = {'SERVER':args.server, 'UID':args.uid, 'PWD':args.pwd}
    input_sheets = get_sheets(args.workbook, sheet_name_substr='TPO-output') 
    points = get_points(input_sheets)
    create_tpocom_output_tables(db_server, points)
    create_tracker_tables(db_server, points)