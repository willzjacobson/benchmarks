import cfgparse

class paramConfigParser:
	
	
	
	def __init__(self, ConfigFileName, ConfigFileKey):
		self.ConfigFileKey = ConfigFileKey;
		self.cparser = cfgparse.ConfigParser()
		
		''' added by ashwath for Weather '''
		self.cparser.add_option('weather_obs_table_name', dest='weatherObsTableName', type='string',keys=self.ConfigFileKey)
		self.cparser.add_option('weather_hour_table_name', dest='weatherHourTableName', type='string',keys=self.ConfigFileKey)
		self.cparser.add_option('weather_DB', dest='weatherDB', type ='string', keys=self.ConfigFileKey)
		''' added by ashwath for occupancy '''
		self.cparser.add_option('SERVER', dest='server', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('DB', dest='db', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('UID', dest='uid', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('PWD', dest='pwd', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('startup_table_name', dest='startupTableNameList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('output_startup', dest='outputStartup', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('output_rampdown', dest='outputRampdown', type='string', keys=self.ConfigFileKey)
		
		self.cparser.add_option('building_open_hour', dest='openHour', type='string', keys=self.ConfigFileKey)
		
		
		self.cparser.add_file(ConfigFileName)
		
	''' added by ashwath for weather '''
	def weatherObsTableName(self):
		options = self.cparser.parse()
		rstring = options.weatherObsTableName
		return rstring

	def weatherHourTableName(self):
		options = self.cparser.parse()
		rstring = options.weatherHourTableName
		return rstring
		
	def weatherDB(self):
		options = self.cparser.parse()
		return options.weatherDB



	def startupTableNameList(self):
		options = self.cparser.parse()
		rstring = options.startupTableNameList
		rstring = rstring.replace(' ', '')
		rlist = rstring.split(',')
		
		return rlist
		

		
	def startupTableName(self, table_number=0):
		rlist = self.startupTableNameList()
		return rlist[table_number]
		

		
	def server(self):
		options = self.cparser.parse()
		return options.server
		
	def database(self):
		options = self.cparser.parse()
		return options.db
		
	def uid(self):
		options = self.cparser.parse()
		return options.uid
		
	def pwd(self):
		options = self.cparser.parse()
		return options.pwd
		
	def outputRampDownTable(self):
		options = self.cparser.parse()
		return options.outputRampdown
		
	def outputStartUpTable(self):
		options = self.cparser.parse()
		return options.outputStartup
		
	def openHour(self):
		options = self.cparser.parse()
		return options.openHour
	
	
	def parseString(self, string, seperator):
		rlist = []
		element = ''
		
		for char in list(string):
			if char == ' ':
				continue
			elif char == seperator:
				rlist.append(element)
				element = ''
			else:
				element = element + char
	
		rlist.append(element)
		return rlist




