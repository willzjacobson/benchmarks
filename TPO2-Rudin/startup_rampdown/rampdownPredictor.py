from change_point_SVM.changePointSVM import changePointSVMBase
from data_tools.dataCollectors import *

class universalRampdownPredictor(changePointSVMBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)

    def readFromDB(self):
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName,
                                                                             self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList,
                                                                             self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
        self.SptPredictionsDataCollector.getData()

        if self.paramObj.steamPredictionParams.hasSteamSupply:
            self.SteamPredictionsDataCollector = dataCollectorSteamPredictions(self.conn, self.cursor,
                                                                             self.paramObj.steamPredictionParams.tableName,
                                                                           self.numberOfDays, self.startDatetime, includeWeekends=False)
            self.SteamPredictionsDataCollector.getData()
            
        self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                        self.paramObj.electricityPredictionParams.tableName,
                                                                                        self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.ElectricityPredictionsDataCollector.getData()

        if self.paramObj.occupancyParams.predictOccupancy:

            self.OccupancyPredictionsDataCollector = dataCollectorOccupancyPredictions(self.conn, self.cursor,
                                                                            self.paramObj.occupancyParams.tableName, self.numberOfDays, self.startDatetime, includeWeekends=False)
            self.OccupancyPredictionsDataCollector.getData()


        if self.paramObj.ConfigFileKey == '345_Park':
            self.rampdownDataCollector = dataCollectorParkRampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1), includeWeekends=False)
        elif self.paramObj.ConfigFileKey == '560_Lex':
            self.rampdownDataCollector = dataCollectorLexRampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1), includeWeekends=False)
        elif self.paramObj.ConfigFileKey == '40E52':
        
            self.rampdownDataCollector = dataCollector40E52Rampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1), includeWeekends=False)
        else:#elif self.paramObj.ConfigFileKey == '1BP':
        
            self.rampdownDataCollector = dataCollector1BPRampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1), includeWeekends=False)
        self.rampdownDataCollector.getData()
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

        if self.paramObj.occupancyParams.predictOccupancy:
            self.trajectoryCalculatorNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
            self.generateSinglePointDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
            self.generateCumulativeValueNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)        
            self.generateChangeDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        
        self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateCumulativeValueFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateChangeDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        
        self.generateTimeData()
        
        self.generateOutputData(self.rampdownDataCollector.rawDataKeyDay)
        print "covariates generated from database data..."

    def commitFinalPrediction(self, tableName= None):
        if tableName == None:
            tableName = self.paramObj.rampdownParams.outputRampdown
        if self.finalPrediction.time() > self.paramObj.buildingCloseHour or self.finalPrediction.time() < self.relevantHoursTuple[0]:
            finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(19,00))
            print "final prediction outside relevant hours bound"
        else:
            finalPrediction = self.finalPrediction
        query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
        query += self.runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(finalPrediction) +"' )"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print "final rampdown time committed as " + str(finalPrediction)
        except:
            print "final commit failed... exiting"
            return
        print "final rampdown time committed."


class rampdownPredictorPark(changePointSVMBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)

    def readFromDB(self):
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName,
                                                                             self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList,
                                                                             self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
        self.SptPredictionsDataCollector.getData()
        self.SteamPredictionsDataCollector = dataCollectorSteamPredictions(self.conn, self.cursor,
                                                                             self.paramObj.steamPredictionParams.tableName,
                                                                           self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.SteamPredictionsDataCollector.getData()
        self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                        self.paramObj.electricityPredictionParams.tableName,
                                                                                        self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.ElectricityPredictionsDataCollector.getData()

        self.OccupancyPredictionsDataCollector = dataCollectorOccupancyPredictions(self.conn, self.cursor,
                                                                        self.paramObj.occupancyParams.tableName, self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.OccupancyPredictionsDataCollector.getData()
        
        self.ParkRampdownDataCollector = dataCollectorParkRampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1), includeWeekends=False)
        self.ParkRampdownDataCollector.getData()
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

        self.trajectoryCalculatorNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        self.generateSinglePointDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        self.generateCumulativeValueNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)        
        self.generateChangeDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        
        self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateCumulativeValueFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateChangeDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        
        self.generateTimeData()
        
        self.generateOutputData(self.ParkRampdownDataCollector.rawDataKeyDay)
        print "covariates generated from database data..."

    def commitFinalPrediction(self, tableName):
        if self.finalPrediction.time() > datetime.time(19,00) or self.finalPrediction.time() < self.relevantHoursTuple[0]:
            finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(19,00))
            print "final prediction outside relevant hours bound"
        else:
            finalPrediction = self.finalPrediction
        query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
        query += self.runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(finalPrediction) +"' )"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print "final rampdown time committed as " + str(finalPrediction)
        except:
            print "final commit failed... exiting"
            return
        print "final rampdown time committed."

    
class rampdownPredictorLex(changePointSVMBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime,
                 predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        changePointSVMBase.__init__(self, conn, cursor, paramObj, numberOfDays,startDatetime,
                                      predictionTimestep, performGridSearch,trajectorySizes, relevantHoursTuple)
            
    def readFromDB(self):
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName,
                                                                             self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList,
                                                                             self.paramObj.sptPredictionParams.tableFloorDesignator, includeWeekends=False)
        self.SptPredictionsDataCollector.getData()
        self.ElectricityPredictionsDataCollector = dataCollectorElectricityPredictions(self.conn, self.cursor,
                                                                                        self.paramObj.electricityPredictionParams.tableName,
                                                                                        self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.ElectricityPredictionsDataCollector.getData()

        self.OccupancyPredictionsDataCollector = dataCollectorOccupancyPredictions(self.conn, self.cursor,
                                                                        self.paramObj.occupancyParams.tableName, self.numberOfDays, self.startDatetime, includeWeekends=False)
        self.OccupancyPredictionsDataCollector.getData()
        
        self.LexRampdownDataCollector = dataCollectorLexRampdown(self.conn, self.cursor, self.paramObj.rampdownParams.tableName,
                                                                      self.numberOfDays - 1, self.startDatetime +datetime.timedelta(-1),includeWeekends=False)
        self.LexRampdownDataCollector.getData()
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

        self.trajectoryCalculatorNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        self.generateSinglePointDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        self.generateCumulativeValueNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)        
        self.generateChangeDataNoFloor(self.OccupancyPredictionsDataCollector.rawDataKeyDay)
        
        self.generateTimeData()
        
        self.generateOutputData(self.LexRampdownDataCollector.rawDataKeyDay)
        print "covariates generated from database data..."

    def commitFinalPrediction(self, tableName):
        if self.finalPrediction.time() > self.relevantHoursTuple[1] or self.finalPrediction.time() < self.relevantHoursTuple[0]:
            finalPrediction = datetime.datetime.combine(self.startDatetime.date(), datetime.time(7,00))
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
            return
        print "final rampdown time committed."

