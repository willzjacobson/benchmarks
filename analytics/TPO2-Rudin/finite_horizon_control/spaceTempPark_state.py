from state_cost_base import state_cost_base
from data_tools.dataCollectors import *
import numpy as np
from rpy2.robjects.packages import importr
from rpy2 import robjects


class spaceTempPark_state(state_cost_base):
    def __init__(self,conn,cursor,paramObj, numberOfDays, startDatetime):
        state_cost_base.__init__(self,conn,cursor,paramObj, numberOfDays, startDatetime)
        self.xListFloorData = []
        self.xListNoFloorData = []
        self.m = None
        self.n= None
        self.xKeyFloor= None
        self.gp = {}

    def readFromDB(self):
        self.SptDataCollector =  dataCollectorBMSInput(self.conn, self.cursor,
                                                        self.paramObj.sptParams.tableName, self.numberOfDays, self.startDatetime,
                                                        True, self.paramObj.sptParams.equalityConstraintList,
                                                        self.paramObj.sptParams.constraintValListKeyFloor)
        self.SptDataCollector.getData()
        #space temp predictions should be collected till end of the day
        self.SptPredictionsDataCollector = dataCollectorSpaceTempPredictions(self.conn, self.cursor,
                                                                             self.paramObj.sptPredictionParams.tableName, self.numberOfDays, self.startDatetime.replace(hour=23, minute=59),
                                                                             self.paramObj.floorList, self.paramObj.sptPredictionParams.tableFloorDesignator)
        self.SptPredictionsDataCollector.getData()
        self.SatSPDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                        self.paramObj.satSPParams.tableName, self.numberOfDays, self.startDatetime,
                                                        True, self.paramObj.satSPParams.equalityConstraintList,
                                                        self.paramObj.satSPParams.constraintValListKeyFloor)
        self.SatSPDataCollector.getData()
        
        # steam predictions should be collected till end of day
        self.SteamPredictionsDataCollector = dataCollectorSteamPredictions(self.conn, self.cursor,
                                                                            self.paramObj.steamPredictionParams.tableName,
                                                                            self.numberOfDays, self.startDatetime.replace(hour=23, minute=59), includeWeekends=True)
        self.SteamPredictionsDataCollector.getData()

    def generateCovariates(self):
        self.generateSinglePointDataFloorData(self.SptDataCollector.rawDataKeyDayKeyFloor) #estimated xListFloorData[0]
        self.generateSinglePointDataFloorData(self.SatSPDataCollector.rawDataKeyDayKeyFloor) #control lever xListFloorData[1]
        self.generateSinglePointDataFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor) # xListFloorData[2]
        self.generateSinglePointDataNoFloor(self.SteamPredictionsDataCollector.rawDataKeyDay) # xListNoFloorData[0]

        self.generateOutputData()
        #self.generateHourData()

    def generateDPList(self):
        self.state_populateDPListFloorData(self.SptPredictionsDataCollector.rawDataKeyDayKeyFloor)
        self.state_populateDPListNoFloorData(self.SteamPredictionsDataCollector.rawDataKeyDay)

    def DPMatrixify(self, horizon):
        ''' The architecture of the DP routine could be improved upon, here i'm hard coding a lot of stuff in...'''
        #horizon is the number of timesteps for which the DP matrix will be made
        self.mDP = horizon
        self.nDP = self.n
        self.DPMats = {}

        # find start time by finding value of startDatetime and rounding down to nearest 15 minute value

        self.DPStart = None
        self.startDatetime = self.startDatetime.replace(second = 0, microsecond = 0)
        sdtMin = self.startDatetime.minute
        if sdtMin < 15:
            sdtMin = 0
        elif sdtMin < 30:
            sdtMin = 15
        elif sdtMin < 45:
            sdtMin = 30
        else:
            sdtMin = 45

        self.DPStart= self.startDatetime.replace(minute = sdtMin)

        fifteenMinutes = datetime.timedelta(minutes=15)
        

        #right now, we make the assumption that the first column is the estimated value, the second column is the control, and the rest are to be DP'd upon
        for floor in self.paramObj.floorList:
            self.DPMats[floor] = np.zeros((self.mDP, self.nDP[floor])) # weird coding with nDP
            rowCount = 0

            firstTempVal =self.xListFloorData[0][floor][self.DPStart]
            firstControlVal = self.xListFloorData[1][floor][self.DPStart]
            for n in range(horizon):
                if rowCount > self.mDP:
                    print "uneven length in yList per floor, breaking matrix assigment loop"
                    break
                ts = self.DPStart + n*fifteenMinutes
                if n == 0:
                    self.DPMats[floor][rowCount][0] = firstTempVal
                    self.DPMats[floor][rowCount][1] = firstControlVal
                else:
                    self.DPMats[floor][rowCount][0] = -1
                    self.DPMats[floor][rowCount][1] = -1
                colCount = 2
                for data in DPListFloorData:
                    if ts in data[floor]:
                        self.DPMats[floor][rowCount][colCount] = data[floor][ts]
                        colCount +=1
                    else:
                        self.DPMats[floor][rowCount][colCount] = 0
                        colCount +=1
                        print "error in making DP matrix, abort abort abort!!!"

                for data in DPListNoFloorData:
                    if ts in data:
                        self.DPMats[floor][rowCount][colCount] = data[ts]
                        colCount += 1
                    else:
                        self.DPMats[floor][rowCount][colCount] = 0
                        colCount +=1
                        print "error in making DP matrix, abort abort abort!!!"
                rowCount +=1

                    
                
            


    def generateOutputData(self):
        self.yKeyFloorKeyTS = {}
        for date in self.SptDataCollector.rawDataKeyDayKeyFloor:
            for floor in self.SptDataCollector.rawDataKeyDayKeyFloor[date]:
                if floor not in self.yKeyFloorKeyTS:
                    self.yKeyFloorKeyTS[floor] = {}
                for ts, value in self.SptDataCollector.rawDataKeyDayKeyFloor[date][floor]:
                    newTS = ts + datetime.timedelta(minutes=-15)
                    self.yKeyFloorKeyTS[floor][newTS] = value
                

    def matrixify(self):
        # find m -- the number of overlapping times between yKeyFloorKeyTS for a random floor
        # and the first entry in xListNoFloorData
        self.XKeyFloor = {}
        self.yKeyFloor = {}
        self.m = {}
        self.n = {}
        for floor in self.paramObj.floorList:
            someXData = self.xListFloorData[0][floor]
            validTS = []
            for ts in self.yKeyFloorKeyTS[floor]:
                if ts in someXData:
                    validTS.append(ts)
            print "length of valid TS list for floor " + str(floor) + ": " + str(len(validTS))
            self.m[floor] = len(validTS)
            self.n[floor] = len(self.xListFloorData)
            self.n[floor] += len(self.xListNoFloorData)
            self.XKeyFloor[floor] = np.zeros((self.m[floor], self.n[floor]))
            self.yKeyFloor[floor] = np.zeros(self.m[floor])
            rowCount = 0
            for ts in validTS:
                if rowCount > self.m:
                    print "uneven length in yList per floor, breaking matrix assigment loop"
                    break
                colCount = 0
                for data in self.xListFloorData:
                    if ts in data[floor]:
                        self.XKeyFloor[floor][rowCount, colCount] = data[floor][ts]
                        colCount +=1
                    else:
                        self.XKeyFloor[floor][rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in xList floor data "
                        colCount = colCount + 1
                for data in self.xListNoFloorData:
                    if ts in data:
                        self.XKeyFloor[floor][rowCount, colCount] = data[ts]
                        colCount = colCount + 1
                    else:
                        self.XKeyFloor[floor][rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in xList no floors"
                        colCount = colCount + 1
                if ts in self.yKeyFloorKeyTS[floor]:
                    self.yKeyFloor[floor][rowCount] = self.yKeyFloorKeyTS[floor][ts]
                else:
                    self.yKeyFloor[floor][rowCount] = 0.0001
                    print "timestamp value  " + str(ts) + " not found for output"
                rowCount = rowCount + 1

    def trainGP(self):
        self.gp = {}
        for floor in self.paramObj.floorList:
            floor_noQuotes = str(floor).replace("'", "")
            gpState_R = robjects.r("source('stateGP.R')")
            xloc = "'C:/Rudin/finite_horizon_control/state/dataMatrices/X" + floor_noQuotes + ".csv'"
            yloc = "'C:/Rudin/finite_horizon_control/state/dataMatrices/y" + floor_noQuotes + ".csv'"
            self.gp[floor] = robjects.r("stateGP(" + xloc + ", " + yloc + ", " + floor + ")")

    def loadGP(self, floor):
        floor_noQuotes = str(floor).replace("'", "")
        agp = robjects.r("load('state/gps/gp" + floor_noQuotes + ".gpr')")

    def predictGP(self, floor, xvals):
        floor_noQuotes = str(floor).replace("'","")
        pred= gptk.gpPosteriorMeanVar(robjects.r('myGP_opt' + floorNoQuotes), robjects.r.matrix(xvals, nrow = 4), robjects.r('varsigma.return = TRUE'))
        return pred



    def writeMatricesToFile(self):
        for floor in self.paramObj.floorList:
            np.savetxt('state/dataMatrices/X' + str(floor).replace("'", "")+ '.csv', self.XKeyFloor[floor], delimiter = ',')
            np.savetxt('state/dataMatrices/y' + str(floor).replace("'", "")+ '.csv', self.yKeyFloor[floor], delimiter = ',')
