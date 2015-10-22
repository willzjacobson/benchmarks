
import pyodbc
import datetime
import sys, os

from optparse import OptionParser
import cfgparse


def main():
	cparser = cfgparse.ConfigParser()
	#oparser.add_option("-c", "--class", dest="type", help="Class of the new database", metavar=" Park | Lex | Generic | GenericNoSteam")
	cparser.add_option('DATABASE_CLASS', dest='type', type='string')
	cparser.add_option('SERVER', dest='server', type='string')
	cparser.add_option('MAIN_DATABASE', dest='main', type='string')
	cparser.add_option('UID', dest='login', type='string')
	cparser.add_option('PWD', dest='pwd', type='string')
	cparser.add_option('WEATHER_DATABASE', dest='weather', type='string')
	cparser.add_option('TPOCOM_DATABASE', dest='tpocom', type='string')
	
	cparser.add_file('config.ini')
	
	options = cparser.parse()
	
	sqlscript = {'main': options.type, 'weather': 'weather', 'tpocom': 'tpocom'}
	#sqlscript = {'weather': 'weather'}
	
	
	cnxn = pyodbc.connect("DRIVER={SQL SERVER};SERVER="+options.server+";DATABASE="+'master'+";UID="+options.login+";PWD="+options.pwd)
	cnxn.autocommit = True
	cursor = cnxn.cursor()
	cursor.execute("CREATE DATABASE " + options.main)
	cursor.execute("CREATE DATABASE " + options.weather)
	cursor.execute("CREATE DATABASE " + options.tpocom)
	cursor.close()
	cnxn.close()
	
	for database in sqlscript:
		exec("db = options."+database)
		#print "DRIVER={SQL SERVER};SERVER="+options.server+";DATABASE="+db+";UID="+options.login+";PWD="+options.pwd
		cnxn = pyodbc.connect("DRIVER={SQL SERVER};SERVER="+options.server+";DATABASE="+db+";UID="+options.login+";PWD="+options.pwd)
		cursor = cnxn.cursor()
		
		file = open("Model/"+str(sqlscript[database])+'.sql', 'r')
		script = file.read()
		script = script.replace('$database$', db)
		out = open('output.sql', 'w')
		out.write(script)

		
		sqlQuery = ''
		with open('output.sql', 'r') as inp:
			for line in inp:
				if line == 'GO\n':
					cursor.execute(sqlQuery)
					sqlQuery = ''
				elif 'PRINT' in line:
					disp = line.split("'")[1]
					print(disp, '\r')
				else:
					sqlQuery = sqlQuery + line
		inp.close()
		
		print database + " database successfully created."
		
		cursor.commit()
		cursor.close()
		cnxn.close()
	
	
	
	
main()