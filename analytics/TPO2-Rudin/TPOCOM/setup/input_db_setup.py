'''
Main for setting up TPO input databases.
'''
import sys
import argparse
from workbook_helper import get_sheets, get_points
from db_helper import create_tpocom_input_tables

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description =
                                        'Creates database for receiving '
                                        'new building data from SIF.')
    parser.add_argument('workbook',help='path to pointlist workbook')
    parser.add_argument('server', help='database server address')
    parser.add_argument('uid', help='database user id')
    parser.add_argument('pwd', help='database user password')
    
    args = parser.parse_args()
    db_server = {'SERVER':args.server, 'UID':args.uid, 'PWD':args.pwd}
    input_sheets = get_sheets(args.workbook, sheet_name_substr='TPO-input')
    create_tpocom_input_tables(db_server, get_points(input_sheets))