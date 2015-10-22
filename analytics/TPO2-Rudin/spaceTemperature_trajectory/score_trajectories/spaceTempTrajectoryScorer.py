import spaceTemperature_trajectory.spaceTempTrajectory as spaceTempTrajectory
from data_tools.dataCollectors import *
import data_tools.parameterObject as parameterObject

class spaceTemperatureTrajectoryScorerBase():
    def __init__(self, conn, cursor, paramObj, startDatetime, predictionTimestep,
                 relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59))):
        self.runDatetime = datetime.datetime.now()
        self.conn = conn
        self.cursor = cursor
        self.paramObj = paramObj
        self.runDatetime = datetime.datetime.now()
        self.startDatetime = startDatetime
        self.relevantHoursTuple = relevantHoursTuple
        self.predictionTimestep = predictionTimestep
        self.trajectoryDataKeyFloorKeyTS = None
        self.spaceTemperatureDataKeyFloorKeyTS = None
        self.scoreKeyFloor = None

    def readFromDB(self):
        pass

    def organizeData(self):
        '''
        put the data into self.trajectoryDataKeyFloor,
        self.spaceTemperatureDataKeyFloor and self. maxTS4
        '''
        pass

    def borrowData(self):
        pass

    def autorun(self):
        self.organizeData()
        self.scoreMSE()
        for floor in self.scoreKeyFloor:
            print "floor " + str(floor) + ": " + str(self.scoreKeyFloor[floor])

    def scoreMSE(self):
        self.scoreKeyFloor = {}
        for floor in self.paramObj.floorList:
            tempScore = 0
            nCounter = 0
            for ts in self.spaceTemperatureDataKeyFloorKeyTS[floor]:
                if ts not in self.trajectoryDataKeyFloorKeyTS[floor]:
                    continue
                sptVal = self.spaceTemperatureDataKeyFloorKeyTS[floor][ts]
                trajVal = self.trajectoryDataKeyFloorKeyTS[floor][ts]
                nCounter+=1
                tempScore += (sptVal - trajVal)*(sptVal - trajVal)
            self.scoreKeyFloor[floor] = tempScore/nCounter
        
            
            
class spaceTemperatureTrajectoryScorerPark(spaceTemperatureTrajectoryScorerBase):
    def __init__(self, conn, cursor, paramObj, startDatetime, predictionTimestep,
                 relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59))):
        spaceTemperatureTrajectoryScorerBase.__init__(self, conn, cursor, paramObj, startDatetime, predictionTimestep,
                 relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59)))

    def readFromDB(self):
        self.SpaceTempDataCollector = dataCollectorSpaceTemp(self.conn, self.cursor,
                                                                    self.paramObj.sptParams.tableNameList,
                                                                    0, self.startDatetime, self.paramObj.floorList,
                                                                    self.paramObj.sptParams.floorsKeyTableName)
        self.SpaceTempDataCollector.getData()
        self.SpaceTempTrajectoriesDataCollector = dataCollectorSpaceTempTrajectories(self.conn, self.cursor,
                                                self.paramObj.sptTrajectoryParams.tableName,
                                                0, self.startDatetime,
                                                self.paramObj.floorList,
                                                self.paramObj.sptTrajectoryParams.tableFloorDesignator,
                                                self.predictionTimestep)
        self.SpaceTempTrajectoriesDataCollector.getData()

    def borrowData(self, externalSpaceTempDataCollector, externalSpaceTempTrajectoriesDataCollector):
        self.SpaceTempDataCollector = externalSpaceTempDataCollector
        self.SpaceTempTrajectoriesDataCollector = externalSpaceTempTrajectoriesDataCollector

    def organizeData(self):
        trajData = self.SpaceTempTrajectoriesDataCollector.rawDataKeyDayKeyFloor
        sptData = self.SpaceTempDataCollector.rawDataKeyDayKeyFloor
        self.trajectoryDataKeyFloorKeyTS = {}
        self.spaceTemperatureDataKeyFloorKeyTS = {}
        if len(trajData) > 1 or len(sptData) > 1:
            print "more than one day of data read in! :("
        for date in trajData:
            for floor in trajData[date]:
                if floor not in self.trajectoryDataKeyFloorKeyTS:
                    self.trajectoryDataKeyFloorKeyTS[floor] = {}
                for ts, val in trajData[date][floor]:
                    self.trajectoryDataKeyFloorKeyTS[floor][ts] = val
        for date in sptData:
            for floor in sptData[date]:
                if floor not in self.spaceTemperatureDataKeyFloorKeyTS:
                    self.spaceTemperatureDataKeyFloorKeyTS[floor] = {}
                for ts, val in sptData[date][floor]:
                    self.spaceTemperatureDataKeyFloorKeyTS[floor][ts] = val


class spaceTemperatureTrajectoryScorerLex(spaceTemperatureTrajectoryScorerBase):
    def __init__(self, conn, cursor, paramObj, startDatetime, predictionTimestep,
                 relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59))):
        spaceTemperatureTrajectoryScorerBase.__init__(self, conn, cursor, paramObj, startDatetime, predictionTimestep,
                 relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59)))

    def readFromDB(self):
        self.SpaceTempDataCollector = dataCollectorLexingtonPointNameData(self.conn, self.cursor,
                                                                    self.paramObj.sptParams.tableName,
                                                                    0, self.startDatetime, self.paramObj.floorList,
                                                                    self.paramObj.sptParams.pointName,
                                                                    self.paramObj.sptParams.tableFloorDesignator)
        self.SpaceTempDataCollector.getData()
        self.SpaceTempTrajectoriesDataCollector = dataCollectorSpaceTempTrajectories(self.conn, self.cursor,
                                                self.paramObj.sptTrajectoryParams.tableName,
                                                0, self.startDatetime,
                                                self.paramObj.floorList,
                                                self.paramObj.sptTrajectoryParams.tableFloorDesignator,
                                                self.predictionTimestep)
        self.SpaceTempTrajectoriesDataCollector.getData()

    def borrowData(self, externalSpaceTempDataCollector, externalSpaceTempTrajectoriesDataCollector):
        self.SpaceTempDataCollector = externalSpaceTempDataCollector
        self.SpaceTempTrajectoriesDataCollector = externalSpaceTempTrajectoriesDataCollector

    def organizeData(self):
        trajData = self.SpaceTempTrajectoriesDataCollector.rawDataKeyDayKeyFloor
        sptData = self.SpaceTempDataCollector.rawDataKeyDayKeyFloor
        self.trajectoryDataKeyFloorKeyTS = {}
        self.spaceTemperatureDataKeyFloorKeyTS = {}
        if len(trajData) > 1 or len(sptData) > 1:
            print "more than one day of data read in! :("
        for date in trajData:
            for floor in trajData[date]:
                if floor not in self.trajectoryDataKeyFloorKeyTS:
                    self.trajectoryDataKeyFloorKeyTS[floor] = {}
                for ts, val in trajData[date][floor]:
                    self.trajectoryDataKeyFloorKeyTS[floor][ts] = val
        for date in sptData:
            for floor in sptData[date]:
                if floor not in self.spaceTemperatureDataKeyFloorKeyTS:
                    self.spaceTemperatureDataKeyFloorKeyTS[floor] = {}
                for ts, val in sptData[date][floor]:
                    self.spaceTemperatureDataKeyFloorKeyTS[floor][ts] = val
        
        

    
