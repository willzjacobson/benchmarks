from trajectory_predictor.trajectoryPredictor import trajectoryPredictorBase
from data_tools.dataCollectors import *

class universalTrajectoryPredictor(trajectoryPredictorBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        trajectoryPredictorBase.__init__(self,conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple)
    def readFromDB(self):
        # read data from database
        if 'sat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            self.SatDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.satParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.satParams.equalityConstraintList,
                                                    self.paramObj.satParams.constraintValListKeyFloor)
            self.SatDataCollector.getData()
        if 'rat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            self.RatDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                           self.paramObj.ratParams.tableName, self.numberOfDays, self.startDatetime,
                                                           True, self.paramObj.ratParams.equalityConstraintList,
                                                        self.paramObj.ratParams.constraintValListKeyFloor)
            self.RatDataCollector.getData()
        if 'sats' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            self.SatSPDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                           self.paramObj.satSPParams.tableName, self.numberOfDays, self.startDatetime,
                                                           True, self.paramObj.satSPParams.equalityConstraintList,
                                                        self.paramObj.satSPParams.constraintValListKeyFloor)
            self.SatSPDataCollector.getData()
            
            
        self.SptDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.sptParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.sptParams.equalityConstraintList,
                                                    self.paramObj.sptParams.constraintValListKeyFloor)
        self.SptDataCollector.getData()
        if self.paramObj.sptTrajectoryParams.hasQuadrants:
            self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName, self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList, self.paramObj.sptPredictionParams.tableFloorDesignator, True, self.paramObj.quadrantKeyFloor)
        else:            
            self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName, self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList, self.paramObj.sptPredictionParams.tableFloorDesignator, True)
        self.SptPredictionsDataCollector.getData()
        

    def borrowData(self, externalObject):
        # take data from object which has already read in appropriate data
        if 'rat' in self.paramObj.sptTrajectoryParams.sat_or_rat and 'rat' in externalObject.paramObj.sptTrajectoryParams.sat_or_rat:
            self.RatDataCollector = externalObject.RatDataCollector
        if 'sat' in self.paramObj.sptTrajectoryParams.sat_or_rat and 'sat' in externalObject.paramObj.sptTrajectoryParams.sat_or_rat:
            self.SatDataCollector = externalObject.SatDataCollector
        if 'sats' in self.paramObj.sptTrajectoryParams.sat_or_rat and 'sats' in externalObject.paramObj.sptTrajectoryParams.sat_or_rat:
            self.SatSPDataCollector = externalObject.SatSPDataCollector
        self.SptDataCollector = externalObject.SptDataCollector
        self.SptPredictionsDataCollector = externalObject.SptPredictionsDataCollector

        print "Data borrowed successfully"

    def generateCovariates(self):
        # Generate Data from database data
        if 'rat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for RAT..."
            self.trajectoryCalculator(self.RatDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.RatDataCollector.rawDataKeyDayKeyFloor)
        if 'sat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for SAT..."
            self.trajectoryCalculator(self.SatDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.SatDataCollector.rawDataKeyDayKeyFloor)
        if 'satS' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for SAT SP..."
            self.trajectoryCalculator(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
        print "generating covs for space temp"
        self.trajectoryCalculator(self.SptDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateSinglePointData(self.SptDataCollector.rawDataKeyDayKeyFloor)
        self.generateSinglePointData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        print "generating Hour Data..."
        self.generateHourData()
        print "generating output data..."
        self.generateOutputData(self.SptDataCollector.rawDataKeyDayKeyFloor)


    def generateCovariatesGimp(self):
        # Generate Data from database data
        if 'rat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for RAT..."
            #self.trajectoryCalculator(self.RatDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.RatDataCollector.rawDataKeyDayKeyFloor)
        if 'sat' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for SAT..."
            #self.trajectoryCalculator(self.SatDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.SatDataCollector.rawDataKeyDayKeyFloor)
        if 'satS' in self.paramObj.sptTrajectoryParams.sat_or_rat:
            print "generating covs for SAT SP..."
            #self.trajectoryCalculator(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
            self.generateSinglePointData(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
        print "generating covs for space temp"
        #self.trajectoryCalculator(self.SptDataCollector.rawDataKeyDayKeyFloor)
        #self.trajectoryCalculator(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.generateSinglePointData(self.SptDataCollector.rawDataKeyDayKeyFloor)
        self.generateSinglePointData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        print "generating Hour Data..."
        self.generateHourData()
        print "generating output data..."
        self.generateOutputData(self.SptDataCollector.rawDataKeyDayKeyFloor)

    def commitPredictionsSQL(self, tableName, predictionTimeBase, Run_DateTime):
        ## note that we could commit using maxTS -- however, with the script that has been implemented
        ## to run this prediction, it is easier to use a value for predictionTimeBase + timedelta(predictionTimestep)
        for floor in self.paramObj.floorList:
            if self.paramObj.sptTrajectoryParams.hasQuadrants:
                quad = self.paramObj.quadrantKeyFloor[floor][0]
            else:
                quad = "'NA'"
            query = "insert into " + tableName + " (Run_DateTime, Prediction_DateTime, Value, Floor, Quadrant, Prediction_Timestep) values "
            query += "(" + Run_DateTime.strftime("'%Y-%m-%d %H:%M'") + ","
            query += (predictionTimeBase + datetime.timedelta(0, 900*self.predictionTimestep)).strftime("'%Y-%m-%d %H:%M'") + ","
            query += str(self.finalSptPredictions[floor][0]) + "," + str(floor) +  "," + quad + "," + str(self.predictionTimestep) + ")"
            #print query
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except:
                print "error accessing database tables for write"
        print "Predictions commited for prediction timestep: " + str(self.predictionTimestep) + "..."

class trajectoryPredictorSptPark(trajectoryPredictorBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple, callerPathDirectory):
        trajectoryPredictorBase.__init__(self,conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple, callerPathDirectory)
    def readFromDB(self):
        # read data from database
        self.SatDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.satParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.satParams.equalityConstraintList,
                                                    self.paramObj.satParams.constraintValListKeyFloor)
        self.SatDataCollector.getData()
        self.SptDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.sptParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.sptParams.equalityConstraintList,
                                                    self.paramObj.sptParams.constraintValListKeyFloor)
        self.SptDataCollector.getData()
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName, self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList, self.paramObj.sptPredictionParams.tableFloorDesignator)
        self.SptPredictionsDataCollector.getData()
        self.SatSPDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.satSPParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.satSPParams.equalityConstraintList,
                                                    self.paramObj.satSPParams.constraintValListKeyFloor)
        self.SatSPDataCollector.getData()
        

    def borrowData(self, externalSatDataCollector, externalSptDataCollector, externalSptPredictionsDataCollector, externalSatSPDataCollector):
        # take data from object which has already read in appropriate data
        self.SatDataCollector = externalSatDataCollector
        self.SptDataCollector = externalSptDataCollector
        self.SptPredictionsDataCollector = externalSptPredictionsDataCollector
        self.SatSPDataCollector = externalSatSPDataCollector
        print "Data borrowed successfully"

    def generateCovariates(self):
        # Generate Data from database data
        print "trajectories calculated..."
        self.trajectoryCalculator(self.SptDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.SatDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
        print "generating Hour Data..."
        self.generateHourData()
        print "generating single point for SAT..."
        self.generateSinglePointData(self.SatDataCollector.rawDataKeyDayKeyFloor)
        print "generating single point for SAT SP..."
        self.generateSinglePointData(self.SatSPDataCollector.rawDataKeyDayKeyFloor)
        print "generating output data..."
        self.generateOutputData(self.SptDataCollector.rawDataKeyDayKeyFloor)

    def commitPredictionsSQL(self, tableName, predictionTimeBase, Run_DateTime):
        ## note that we could commit using maxTS -- however, with the script that has been implemented
        ## to run this prediction, it is easier to use a value for predictionTimeBase + timedelta(predictionTimestep)
        for floor in self.paramObj.floorList:
            query = "insert into " + tableName + " (Run_DateTime, Prediction_DateTime, Value, Floor, Quadrant, Prediction_Timestep) values "
            query += "(" + Run_DateTime.strftime("'%Y-%m-%d %H:%M'") + ","
            query += (predictionTimeBase + datetime.timedelta(0, 900*self.predictionTimestep)).strftime("'%Y-%m-%d %H:%M'") + ","
            query += str(self.finalSptPredictions[floor][0]) + "," + str(floor) +  "," + self.paramObj.quadrantKeyFloor[floor][0] + "," + str(self.predictionTimestep) + ")"
            #print query
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except:
                print "error accessing database tables for write"
        print "Predictions commited for prediction timestep: " + str(self.predictionTimestep) + "..."

class trajectoryPredictorSptLex(trajectoryPredictorBase):
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple, callerPathDirectory):
        trajectoryPredictorBase.__init__(self,conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple, callerPathDirectory)


    def readFromDB(self):
        # read data from database
        '''
        self.SatDataCollector = dataCollectorLexingtonPointNameData(self.conn, self.cursor,
                                                       self.paramObj.satParams.tableName, self.numberOfDays, self.startDatetime,
                                                       self.paramObj.floorList, self.paramObj.satParams.pointName,
                                                                    self.paramObj.satParams.tableFloorDesignator, includeWeekends=True)
        self.SatDataCollector.getData()
        '''
        
        self.SptDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.sptParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.sptParams.equalityConstraintList,
                                                    self.paramObj.sptParams.constraintValListKeyFloor)
        self.SptDataCollector.getData()
        
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName, self.numberOfDays, self.startDatetime,
                                                                             self.paramObj.floorList, self.paramObj.sptPredictionParams.tableFloorDesignator)
        self.SptPredictionsDataCollector.getData()
        
        self.RatDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                       self.paramObj.ratParams.tableName, self.numberOfDays, self.startDatetime,
                                                       True, self.paramObj.ratParams.equalityConstraintList,
                                                    self.paramObj.ratParams.constraintValListKeyFloor)
        self.RatDataCollector.getData()

    def borrowData(self, externalSptDataCollector, externalSptPredictionsDataCollector, externalRatDataCollector):
        # take data from object which has already read in appropriate data
        self.SptDataCollector = externalSptDataCollector
        self.SptPredictionsDataCollector = externalSptPredictionsDataCollector
        self.RatDataCollector = externalRatDataCollector
        print "Data borrowed successfully"

    def generateCovariates(self):
        # Generate Data from database data
        print "trajectories calculated..."
        self.trajectoryCalculator(self.SptDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.trajectoryCalculator(self.RatDataCollector.rawDataKeyDayKeyFloor)
        print "generating Hour Data..."
        self.generateHourData()
        print "generating single point for RAT..."
        self.generateSinglePointData(self.RatDataCollector.rawDataKeyDayKeyFloor)
        print "generating output data..."
        self.generateOutputData(self.SptDataCollector.rawDataKeyDayKeyFloor)

    def commitPredictionsSQL(self, tableName, predictionTimeBase, Run_DateTime):
        ## note that we could commit using maxTS -- however, with the script that has been implemented
        ## to run this prediction, it is easier to use a value for predictionTimeBase + timedelta(predictionTimestep)
        for floor in self.paramObj.floorList:
            query = "insert into " + tableName + " (Run_DateTime, Prediction_DateTime, Value, Floor, Quadrant, Prediction_Timestep) values "
            query += "(" + Run_DateTime.strftime("'%Y-%m-%d %H:%M'") + ","
            query += (predictionTimeBase + datetime.timedelta(0, 900*self.predictionTimestep)).strftime("'%Y-%m-%d %H:%M'") + ","
            query += str(self.finalSptPredictions[floor][0]) + "," + str(floor) +  "," + "'" + "NA" + "'," + str(self.predictionTimestep) + ")"
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except:
                print "error accessing database tables for write"
        print "Predictions commited for prediction timestep: " + str(self.predictionTimestep) + "..."
