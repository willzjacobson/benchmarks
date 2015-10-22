#!/bin/env python

import pyodbc


def connect(driver, uid, pwd, database, server):
	# connect to database by building connection string
	cnxn = pyodbc.connect(
		'DRIVER=%s;Server=%s;Database=%s;UID=%s;PWD=%s;Trusted_Connection=No;'
		% (driver, server, database, uid, pwd))
	return (cnxn, cnxn.cursor())

	

if __name__ == '__main__':
	connect()