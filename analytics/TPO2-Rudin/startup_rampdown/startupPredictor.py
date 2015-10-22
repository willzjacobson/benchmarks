from change_point_SVM.changePointSVM import changePointSVMBase
from data_tools.dataCollectors import *

class universalStartupPredictor(changePointSVMBase):
        def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
            changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)

        def readFromDB(self):
            self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                                 self.paramObj.sptPredictionParams.tableName,
                                                                                 self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)),
                                                                                 self.paramObj.floorList,
                                                                                 self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
            self.SptPredictionsDataCollector.getData()
            if self.paramObj.steamPredictionParams.hasSteamSupply:
                self.SteamPredictionsDataCollector = dataCollectorSteamPredictions(self.conn, self.cursor,
                                                                                 self.paramObj.steamPredictionParams.tableName,
                                                                               self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)), includeWeekends=False)
                self.SteamPredictionsDataCollector.getData()
            
            self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                            self.paramObj.electricityPredictionParams.tableName,
                                                                                            self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,00)), includeWeekends=False)
            self.ElectricityPredictionsDataCollector.getData()

            if self.paramObj.ConfigFileKey == '345_Park':
                self.startupDataCollector = dataCollectorBMSInputParkStartup(self.conn, self.cursor, self.paramObj.startupParams.tableName,
                                                                          self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)) +datetime.timedelta(-1),
                                                                             False, self.paramObj.startupParams.equalityConstraintList, self.paramObj.equipmentList)
            elif self.paramObj.ConfigFileKey == '560_Lex':
                self.startupDataCollector = dataCollectorBMSInputLexStartup(self.conn, self.cursor, self.paramObj.startupParams.tableName,
                                                                      self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)) +datetime.timedelta(-1),
                                                                False, self.paramObj.startupParams.equalityConstraintList,
                                                                       self.paramObj.floorListKeyFloor)
            elif self.paramObj.ConfigFileKey == '40E52':
                self.startupDataCollector = dataCollectorBMSInput40E52Startup(self.conn, self.cursor, self.paramObj.startupParams.tableName,
                                                                          self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)) +datetime.timedelta(-1),
                                                                             False, self.paramObj.startupParams.equalityConstraintList, self.paramObj.floorList)

            else:# self.paramObj.ConfigFileKey == '1BP':
                self.startupDataCollector = dataCollectorBMSInput1BPStartup(self.conn, self.cursor, self.paramObj.startupParams.tableName,
                                                                          self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)) +datetime.timedelta(-1),
                                                                             False, self.paramObj.startupParams.equalityConstraintList, self.paramObj.zoneList)                
                
    
            self.startupDataCollector.getData()
            print "database read completed..."
            
        def generateCovariates(self):
            # generate covariates
            self.trajectoryCalculatorFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)

            if self.paramObj.steamPredictionParams.hasSteamSupply:
                self.trajectoryCalculatorNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)
                self.generateSinglePointDataNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)
                self.generateCumulativeValueNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)        
                self.generateChangeDataNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)

            self.trajectoryCalculatorNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
            self.generateSinglePointDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
            self.generateCumulativeValueNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
            self.generateChangeDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
            
            self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
            self.generateCumulativeValueFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
            self.generateChangeDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)


            
            self.generateTimeData()
            
            self.generateOutputData(self.startupDataCollector.rawDataKeyDay)
            print "covariates generated from database data..."

        def commitFinalPrediction(self, tableName = None):
            if tableName == None:
		tableName = self.paramObj.startupParams.outputStartup
	    if self.finalPrediction.time() > self.paramObj.buildingOpenHour or self.finalPrediction.time() < self.relevantHoursTuple[0]:
		finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(self.paramObj.buildingOpenHour) + datetime.timdelta(0,-60*30))
		print "final prediction of " + str(self.finalPrediction) + " outside relevant hours bound"
	    else:
		finalPrediction = self.finalPrediction
	    query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
	    query += self.runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(finalPrediction) +"' )"
	    try:
		self.cursor.execute(query)
		self.conn.commit()
	    except:
		print "final commit failed... exiting"
		return None
	    print "final startup time committed as " + str(finalPrediction)
	    return finalPrediction

class startupPredictorPark(changePointSVMBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)

    def readFromDB(self):
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName,
                                                                             self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)),
                                                                             self.paramObj.floorList,
                                                                             self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
        self.SptPredictionsDataCollector.getData()
        self.SteamPredictionsDataCollector = dataCollectorSteamPredictions(self.conn, self.cursor,
                                                                             self.paramObj.steamPredictionParams.tableName,
                                                                           self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)), includeWeekends=False)
        self.SteamPredictionsDataCollector.getData()
        self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                        self.paramObj.electricityPredictionParams.tableName,
                                                                                        self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,00)), includeWeekends=False)
        self.ElectricityPredictionsDataCollector.getData()

        #self.OccupancyPredictionsDataCollector = dataCollectorOccupancyPredictions(self.conn, self.cursor,self.paramObj.occupancyParams.tableName, self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)), includeWeekends=False)
        #self.OccupancyPredictionsDataCollector.getData()
        
        self.ParkStartupDataCollector = dataCollectorBMSInputParkStartup(self.conn, self.cursor, self.paramObj.startupParams.tableNameList,
                                                                      self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(9,01)) +datetime.timedelta(-1),
                                                                         False, self.paramObj.startupParams.equalityConstraintList, self.paramObj.startupParams.constraintValListKeyTable)
        self.ParkStartupDataCollector.getData()
        print "database read completed..."
        
    def generateCovariates(self):
        # generate covariates
        self.trajectoryCalculatorFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)

        
        self.trajectoryCalculatorNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)
        self.generateSinglePointDataNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)
        self.generateCumulativeValueNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)        
        self.generateChangeDataNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay)

        self.trajectoryCalculatorNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
        self.generateSinglePointDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
        self.generateCumulativeValueNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
        self.generateChangeDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
        
        self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateCumulativeValueFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateChangeDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)


        #self.trajectoryCalculatorNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        #self.generateSinglePointDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        #self.generateCumulativeValueNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)        
        #self.generateChangeDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        
        self.generateTimeData()
        
        self.generateOutputData(self.ParkStartupDataCollector.rawDataKeyDay)
        print "covariates generated from database data..."

    def commitFinalPrediction(self, tableName):
        if self.finalPrediction.time() > datetime.time(7,00) or self.finalPrediction.time() < self.relevantHoursTuple[0]:
            finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(6,30))
            print "final prediction outside relevant hours bound"
        else:
            finalPrediction = self.finalPrediction
        query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
        query += self.runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(finalPrediction) +"' )"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except:
            print "final commit failed... exiting"
            return None
        print "final startup time committed."
        return finalPrediction

    
class startupPredictorLex(changePointSVMBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)
            
    def readFromDB(self):
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName,
                                                                             self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)),
                                                                             self.paramObj.floorList,
                                                                             self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
        self.SptPredictionsDataCollector.getData()
        self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                        self.paramObj.electricityPredictionParams.tableName,
                                                                                        self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)), includeWeekends=False)
        self.ElectricityPredictionsDataCollector.getData()

        #self.OccupancyPredictionsDataCollector = dataCollectorOccupancyPredictions(self.conn, self.cursor,self.paramObj.occupancyParams.tableName, self.numberOfDays, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)), includeWeekends=False)
        #self.OccupancyPredictionsDataCollector.getData()
        
        self.LexStartupDataCollector = dataCollectorBMSInputLexStartup(self.conn, self.cursor, self.paramObj.startupParams.tableName,
                                                                      self.numberOfDays - 1, datetime.datetime.combine(self.startDatetime.date(), datetime.time(12,01)) +datetime.timedelta(-1),
                                                                False, self.paramObj.startupParams.equalityConstraintList,
                                                                       self.paramObj.startupParams.constraintValListKeyFloor)
        self.LexStartupDataCollector.getData()
        print "database read completed..."

    def generateCovariates(self):
        self.trajectoryCalculatorFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)


        self.trajectoryCalculatorNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
        self.generateSinglePointDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)
        self.generateCumulativeValueNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
        self.generateChangeDataNoFloor(self.ElectricityPredictionsDataCollector.rawDataKeyDay)        
        
        self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateCumulativeValueFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateChangeDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)

        #self.trajectoryCalculatorNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        #self.generateSinglePointDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        #self.generateCumulativeValueNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)        
        #self.generateChangeDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        
        self.generateTimeData()
        
        self.generateOutputData(self.LexStartupDataCollector.rawDataKeyDay)
        print "covariates generated from database data..."

    def commitFinalPrediction(self, tableName):
        if self.finalPrediction.time() > datetime.time(8,00) or self.finalPrediction.time() < self.relevantHoursTuple[0]:
            finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(8,00))
            print "final prediction outside relevant hours bound"
        else:
            finalPrediction = self.finalPrediction
        query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
        query += self.runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(finalPrediction) +"' )"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except:
            print "final commit failed... exiting"
            return None
        print "final startup time committed."
        return finalPrediction

