__author__ = 'ashishgagneja'

"""
driver for generating start-time using a sarima model built using space temperature data
"""

import utils.connect as connect
import config

cfg = config.ashish
bldg_params = cfg["park345"]


# connect to database
db = connect.connect(bldg_params['db_server_input'], bldg_params['db_user_input'],
                    pem_file=bldg_params['pem_file_input'])


# query data

# invoke model

# TODO: save results

db.close()