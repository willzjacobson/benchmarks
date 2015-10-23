import cfgparse

class paramConfigParser:
	
	
	
	def __init__(self, ConfigFileName, ConfigFileKey):
		self.ConfigFileKey = ConfigFileKey;
		self.cparser = cfgparse.ConfigParser()
		self.cparser.add_option('building_floors', dest='floorList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('floor_quadrants', dest='quadrantList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('floor_equipments', dest='equipmentsList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_prediction_table_name', dest='sptPredTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_prediction_table_floor_designator', dest='sptPredTableFloorDes', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_table_name', dest='sptTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_equality_constraint_list', dest='sptEqConstraintList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('sat_table_name', dest='satTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('sat_equality_constraint_list', dest='satEqConstraintList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('satS_table_name', dest='satSTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('satS_equality_constraint_list', dest='satSEqConstraintList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('steam_prediction_table_name', dest='steamPredictionTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('elec_prediction_table_name', dest='elecPredictionTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('ramp_down_table_name', dest='rampDownTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('startup_table_name_list', dest='startupTableNameList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('startup_equality_constraint_list', dest='startupEqConstraintList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_trajectory_table_name', dest='sptTrajectoryTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('spt_trajectory_table_floor_designator', dest='sptTrajectoryTableFloorDes', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('rat_table_name', dest='ratTableName', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('rat_equality_constraint_list', dest='ratEqConstraintList', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('SERVER', dest='server', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('DB', dest='db', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('UID', dest='uid', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('PWD', dest='pwd', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('output_startup', dest='outputStartup', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('output_rampdown', dest='outputRampdown', type='string', keys=self.ConfigFileKey)
		self.cparser.add_option('output_space_temp_trajectory', dest='outputSpctempTraj', type='string', keys=self.ConfigFileKey)

		''' added by ashwath for GP control '''
		self.cparser.add_option('steam_table_name', dest='steamTableName', type='string', keys=self.ConfigFileKey)
		''' added by ashwath for Weather '''
		self.cparser.add_option('weather_obs_table_name', dest='weatherObsTableName', type='string',keys=self.ConfigFileKey)
		self.cparser.add_option('weather_hour_table_name', dest='weatherHourTableName', type='string',keys=self.ConfigFileKey)
                self.cparser.add_option('weather_DB', dest='weatherDB', type ='string', keys=self.ConfigFileKey)
                ''' added by ashwath for occupancy '''
                self.cparser.add_option('occupancy_prediction_table_name', dest='occupancyTableName', type='string', keys=self.ConfigFileKey)
		
		self.cparser.add_file(ConfigFileName)

        ''' added by ashwath for GP control'''

        def steamTableName(self):
                options = self.cparser.parse()
		rstring = options.steamTableName
		return rstring

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


        ''' added by ashwath for occupancy  '''
        def occupancyTableName(self):
                options = self.cparser.parse()
                return options.occupancyTableName
                
	
	def floorList(self):
		finalFloorList = []
		options = self.cparser.parse()
		floorListString = options.floorList
		flist = self.parseString(floorListString, ',')
		if flist[0] == 'range':
			flist = range(flist[1], flist[2]+1)
		for floor in flist:
			if len(list(floor)) == 1:
				finalFloorList.append("'F0"+floor+"'")
			else:
				finalFloorList.append("'F"+floor+"'")
		return finalFloorList
		
	def floorListKeyFloor(self):
		rdict = {}
		floorList = self.floorList()
		for i in floorList:
			rdict[i] = [i]
		return rdict
		
	def equipmentNumberKeyFloor(self):
		rdict = {}
		options = self.cparser.parse()
		equipListString = options.equipmentsList
		eqList = self.parseString(equipListString, ',')
		floorList = self.floorList()
		count = 0
		for i in floorList:
			rdict[i] = ["'"+eqList[count]+"'"]
			count = count + 1
		return rdict
		
	def quadrantKeyFloor(self):
		rdict = {}
		options = self.cparser.parse()
		quadListString = options.quadrantList
		qList = self.parseString(quadListString, ',')
		floorList = self.floorList()
		count = 0
		for i in floorList:
			rdict[i] = ["'"+qList[count]+"'"]
			count = count + 1
		return rdict
		
	def sptPredictionTableName(self):
		options = self.cparser.parse()
		rstring = options.sptPredTableName
		return rstring
		
	def sptPredictionTableFloorDesignator(self):
		options = self.cparser.parse()
		rstring = options.sptPredTableFloorDes
		return rstring
		
	def sptTableName(self):
		options = self.cparser.parse()
		rstring = options.sptTableName
		return rstring
		
	def sptEqualityConstraintList(self):
		options = self.cparser.parse()
		rstring  = options.sptEqConstraintList
		rlist = self.parseString(rstring, ',')
		return rlist
		
	def satTableName(self):
		options = self.cparser.parse()
		rstring = options.satTableName
		return rstring
		
	def satEqualityConstraintList(self):
		options = self.cparser.parse()
		rstring  = options.satEqConstraintList
		rlist = self.parseString(rstring, ',')
		return rlist	
		
	def satSTableName(self):
		options = self.cparser.parse()
		rstring = options.satSTableName
		return rstring
		
	def satSEqualityConstraintList(self):
		options = self.cparser.parse()
		rstring  = options.satSEqConstraintList
		rlist = self.parseString(rstring, ',')
		return rlist
		
	def steamPredictionTableName(self):
		options = self.cparser.parse()
		rstring = options.steamPredictionTableName
		return rstring
	
	def electricityPredictionTableName(self):
		options = self.cparser.parse()
		rstring = options.elecPredictionTableName
		return rstring
		
	def rampDownTableName(self):
		options = self.cparser.parse()
		rstring = options.rampDownTableName
		return rstring
		
	def startupTableNameList(self):
		options = self.cparser.parse()
		rstring = options.startupTableNameList
		rlist = self.parseString(rstring, ',')
		return rlist
		
	def startupEqualityConstraintList(self):
		options = self.cparser.parse()
		rstring  = options.startupEqConstraintList
		rlist = self.parseString(rstring, ',')
		return rlist
		
	def startupConstraintValListKeyTable(self):
		rdict = {}
		tableList = self.startupTableNameList()
		count = 1
		for table in tableList:
			self.cparser.add_option('startup_CVKT_list_'+str(count), dest='startupCVLKT', type='string', keys=self.ConfigFileKey)
			options = self.cparser.parse()
			rstring = options.startupCVLKT
			rlist = self.parseString(rstring, ',')
			intList = []
			for element in rlist:
				intList.append("'"+str(element)+"'")
			rdict[table] = intList
			count = count + 1
		return rdict
		
	def sptTrajectoryTableName(self):
		options = self.cparser.parse()
		rstring = options.sptTrajectoryTableName
		return rstring
		
	def sptTrajectoryTableFloorDesignator(self):
		options = self.cparser.parse()
		rstring = options.sptTrajectoryTableFloorDes
		return rstring
		
	def ratTableName(self):
		options = self.cparser.parse()
		rstring = options.ratTableName
		return rstring
		
	def ratEqualityConstraintList(self):
		options = self.cparser.parse()
		rstring  = options.ratEqConstraintList
		rlist = self.parseString(rstring, ',')
		return rlist
		
	def startupTableName(self, table_number=0):
		rlist = self.startupTableNameList()
		return rlist[table_number]
		
	#parses a string of form element1, element2, element3, ..., elementN
	#returns the list [element1, element2, element3, ..., elementN]
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
		
	def outputSpaceTempTrajectoryTable(self):
		options = self.cparser.parse()
		return options.outputSpctempTraj

'''
 #DEBUGING PURPOSE 
		
print "TESTING 345 PARK"
p = paramConfigParser('config_master.json', '345_Park')
print p.floorList()
print p.floorListKeyFloor()
print p.quadrantKeyFloor()
print p.equipmentNumberKeyFloor()
print p.sptPredictionTableName()
print p.sptPredictionTableFloorDesignator()
print p.sptTableName()
print p.sptEqualityConstraintList()
print p.satTableName()
print p.satEqualityConstraintList()
print p.satSTableName()
print p.satSEqualityConstraintList()
print p.steamPredictionTableName()
print p.electricityPredictionTableName()
print p.rampDownTableName()
print p.startupTableNameList()
print p.startupTableName()
print p.startupEqualityConstraintList()
print p.startupConstraintValListKeyTable()
print p.sptTrajectoryTableName()
print p.sptTrajectoryTableFloorDesignator()
#print p.ratTableName()
#print p.ratEqualityConstraintList()
print p.server()
print p.database()
print p.uid()
print p.pwd()
print p.outputStartUpTable()
print p.outputRampDownTable()
print p.outputSpaceTempTrajectoryTable()		
			
print "TESTING 560 LEXINGTON"
p = paramConfigParser('config_master.json', '560_Lex')
print p.floorList()
print p.floorListKeyFloor()
#print p.quadrantKeyFloor()
#print p.equipmentNumberKeyFloor()
print p.sptPredictionTableName()
print p.sptPredictionTableFloorDesignator()
print p.sptTableName()
print p.sptEqualityConstraintList()
print p.satTableName()
print p.satEqualityConstraintList()
#print p.satSTableName()
#print p.satSEqualityConstraintList()
#print p.steamPredictionTableName()
print p.electricityPredictionTableName()
print p.rampDownTableName()
print p.startupTableNameList()
print p.startupTableName()
print p.startupEqualityConstraintList()
#print p.startupConstraintValListKeyTable()
print p.sptTrajectoryTableName()
print p.sptTrajectoryTableFloorDesignator()
print p.ratTableName()
print p.ratEqualityConstraintList()
print p.server()
print p.database()
print p.uid()
print p.pwd()
print p.outputStartUpTable()
print p.outputRampDownTable()
print p.outputSpaceTempTrajectoryTable()
'''

