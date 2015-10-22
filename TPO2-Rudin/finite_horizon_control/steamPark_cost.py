from state_cost_base import state_cost_base
from data_tools.dataCollectors import *
from rpy2.robjects.packages import importr
from rpy2 import robjects
import numpy as np

class steamPark_cost(state_cost_base):
    def __init__(self,conn,cursor,paramObj, numberOfDays, startDatetime):
        state_cost_base.__init__(self,conn,cursor,paramObj, numberOfDays, startDatetime)
        self.xListFloorData = []
        self.xListNoFloorData = []
        self.m = None
        self.n= None
        self.xKeyFloor= None
        self.gp = {}

    def getFinalRecCost(self):
        sdt = self.startDatetime.minute
        if sdt < 15:
            sdt = 0
        elif sdt < 30:
            sdt = 15
        elif sdt < 45:
            sdt = 30
        else:
            sdt = 45
        return self.xListNoFloorData[0][self.startDateTime.replace(minute = sdt)]

    def readFromDB(self):
        self.SptDataCollector =  dataCollectorBMSInput(self.conn, self.cursor,
                                                        self.paramObj.sptParams.tableName, self.numberOfDays, self.startDatetime,
                                                        True, self.paramObj.sptParams.equalityConstraintList,
                                                        self.paramObj.sptParams.constraintValListKeyFloor)
        self.SptDataCollector.getData()
        self.SatSPDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                        self.paramObj.satSPParams.tableName, self.numberOfDays, self.startDatetime,
                                                        True, self.paramObj.satSPParams.equalityConstraintList,
                                                        self.paramObj.satSPParams.constraintValListKeyFloor)
        self.SatSPDataCollector.getData()

        self.SteamDataCollector = dataCollectorBMSInput(self.conn, self.cursor,
                                                        self.paramObj.steamParams.tableName, self.numberOfDays, self.startDatetime,
                                                        True)
        self.SteamDataCollector.getData()

    def generateCovariates(self):
        self.generateSinglePointDataNoFloor(self.SteamDataCollector.rawDataKeyDay) # in data matrix, this is the first value
        self.generateSinglePointDataFloorData(self.SptDataCollector.rawDataKeyDayKeyFloor) # xlist[0 + 2n] 
        self.generateSinglePointDataFloorData(self.SatSPDataCollector.rawDataKeyDayKeyFloor) #xlist[1 + 2n]


        self.generateOutputData()
        #self.generateHourData()
        


    def generateOutputData(self):
        self.yKeyTS = {}
        for date in self.SteamDataCollector.rawDataKeyDay:
            for ts, value in self.SteamDataCollector.rawDataKeyDay[date]:
                newTS = ts + datetime.timedelta(minutes=-15)
                self.yKeyTS[newTS] = value
                

    def matrixify(self):
        # find m -- the number of overlapping times between yKeyFloorKeyTS (which is steam) for a random floor
        # and the first entry in xListNoFloorData, which is also steam
        self.X= {}
        self.y = {}
        self.m = None
        self.n = None 
        someXData = self.xListNoFloorData[0]
        validTS = []
        for ts in self.yKeyTS:
            if ts in someXData:
                validTS.append(ts)
        print "length of valid TS list: " + str(len(validTS))
        self.m = len(validTS)
        self.n = len(self.xListFloorData) * len(self.paramObj.floorList)
        self.n += len(self.xListNoFloorData)
        print "n is: " + str(self.n)
        self.X = np.zeros((self.m, self.n))
        self.y = np.zeros(self.m)
        rowCount = 0
        for ts in validTS:
            if rowCount > self.m:
                print "uneven length in yList per floor, breaking matrix assigment loop"
                break
            colCount = 0
            for data in self.xListNoFloorData:
                if ts in data:
                    self.X[rowCount, colCount] = data[ts]
                    colCount = colCount + 1
                else:
                    self.X[rowCount, colCount] = 0.0001
                    print "timestamp value " + str(ts) + " not found in xList no floors"
                    colCount = colCount + 1
            for data in self.xListFloorData:
                for floor in self.paramObj.floorList:
                    if ts in data[floor]:
                        self.X[rowCount, colCount] = data[floor][ts]
                        colCount +=1
                    else:
                        self.X[rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in xList floor data for floor " + str(floor)
                        colCount = colCount + 1
            if ts in self.yKeyTS:
                self.y[rowCount] = self.yKeyTS[ts]
            else:
                self.y[rowCount] = 0.0001
                print "timestamp value  " + str(ts) + " not found for output"
            rowCount = rowCount + 1

    def trainGP(self):
        gpState_R = robjects.r("source('costGP.R')")
        self.gp = robjects.r("costGP('C:/Rudin/finite_horizon_control/cost/dataMatrices/X.csv', 'C:/Rudin/finite_horizon_control/state/dataMatrices/y.csv')")

    def predictGP(self, xvals):
        pred= gptk.gpPosteriorMeanVar(robjects.r('myGP_opt'), robjects.r.matrix(xvals, nrow = 4), robjects.r('varsigma.return = TRUE'))
        return pred

    def writeMatricesToFile(self):
        np.savetxt('cost/dataMatrices/X.csv', self.X, delimiter = ',')
        np.savetxt('cost/dataMatrices/y.csv', self.y, delimiter = ',')
