import cfgparse

class paramConfigParser:
	
	
	
	def __init__(self, ConfigFileName, ConfigFileKey):
		self.ConfigFileKey = ConfigFileKey;
		self.cparser = cfgparse.ConfigParser()
		self.cparser.add_option('steam_prediction_table_name', dest='steamPredictionTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('SERVER', dest='server', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('DB', dest='db', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('UID', dest='uid', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('PWD', dest='pwd', type='string', keys=self.ConfigFileKey)
		
		#self.cparser.add_option('weather_database', dest='weatherDatabase', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('weather_DB', dest='weatherDatabase', type='string', keys=self.ConfigFileKey)
		#self.cparser.add_option('hourly_forecast', dest='hourlyForecast', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('weather_hour_table_name', dest='hourlyForecast', type='string', keys=self.ConfigFileKey)
		
		self.cparser.add_option('preheat_forecast_table', dest='preheatForecastTable', type='string', keys=self.ConfigFileKey)
		
		#self.cparser.add_option('current_steam_table', dest='currentSteamTable', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('steam_table_name', dest='currentSteamTable', type='string', keys=self.ConfigFileKey)
		
	
		self.cparser.add_option('freeze_protection_threshold', dest='freezeProtection', type='int', keys=self.ConfigFileKey)
		
		self.cparser.add_file(ConfigFileName)
	
		
	def steamPredictionTableName(self):
		options = self.cparser.parse()
		rstring = options.steamPredictionTableName
		return rstring
		
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
		
		
	def hourlyForecast(self):
		options = self.cparser.parse()
		return options.hourlyForecast

	def weatherDatabase(self):
		options = self.cparser.parse()
		return options.weatherDatabase


	def preheatForecastTable(self):
		options = self.cparser.parse()
		return options.preheatForecastTable
		
	def currentSteamTable(self):
		options = self.cparser.parse()
		return options.currentSteamTable
		
	def freezeProtectionThreshold(self):
		options = self.cparser.parse()
		return options.freezeProtection

