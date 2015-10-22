from data_tools.dataCollectors import *
import data_tools.parameterObject as parameterObject
import random
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import pylab as pl
import pyodbc
import cPickle as pickle


class buildingDataMatrixBase():
    def __init__(self,conn,cursor, paramObj, numberOfDays, startDatetime, matrix_per_floor = False relevantHoursTuple = (datetime.time(0,0,0), datetime.time(23,59))):
        self.conn = conn
        self.cursor = cursor
        self.paramObj = paramObj
        self.runDatetime = datetime.datetime.now()
        self.startDatetime = startDatetime
        self.relevantHoursTuple = relevantHoursTuple
        self.numberOfDays = numberOfDays
        self.matrix_per_floor = matrix_per_floor
        self.xListFloorData = []
        self.xListNoFloorData = []
        self.yData = None
        self.xMatrices = None
        self.yMatrices=None
        self.scaler = None
        self.queryVector = None

    def readFromDB(self):
        pass

    def generateCovariates(self):
        pass

    def autorun(self):
        self.generateCovariates()




    '''
    Data Generation Functions
    _________________________
    '''
        

    def generateCumulativeChangeDataFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        prevValKeyFloor = {}
        for day in dataDictKeyDateKeyFloor:
            for floor in dataDictKeyDateKeyFloor[day]:
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                prevValKeyFloor[floor] = None
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    time = ts.time()
                    date = ts.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        prevValKeyFloor[floor] = value
                        continue
                    if prevValKeyFloor[floor] != None:
                        singlePointDataKeyFloorKeyTS[floor][ts] = value-prevValKeyFloor[floor]
                    else:
                        singlePointDataKeyFloorKeyTS[floor][ts] = 0
        self.xListFloorData.append(singlePointDataKeyFloorKeyTS)


    def generateCumulativeChangeDataNoFloor(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            prevVal = None
            for ts, value in dataDictKeyDate[day]:
                prevTs = (ts + datetime.timedelta(0, -300)).time()
                time = ts.time()
                date = ts.date()
                if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                    prevVal = value
                    continue
                if prevVal != None:
                    singlePointDataKeyTS[ts] = value - prevVal
                else:
                    singlePointDataKeyTS[ts] = 0
                prevVal = value
        self.xListNoFloorData.append(singlePointDataKeyTS)
        


    def trajectoryCalculatorFloorData(self, dataDictKeyDateKeyFloor, trajectorySizes):
        maxSpace = np.max(trajectorySizes)
        trajectoryDataKeySizeKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            prevDay = day+ datetime.timedelta(-1)
            for size in trajectorySizes:
                if size not in trajectoryDataKeySizeKeyFloorKeyTS:
                    trajectoryDataKeySizeKeyFloorKeyTS[size] = {}
                for floor in self.paramObj.floorList:
                    if floor not in trajectoryDataKeySizeKeyFloorKeyTS[size]:
                        trajectoryDataKeySizeKeyFloorKeyTS[size][floor] = {}
                    for i in range(0, len(dataDictKeyDateKeyFloor[day][floor])):
                        timestamp, value = dataDictKeyDateKeyFloor[day][floor][i]
                        if i >= size:
                            pastTS, pastVal = dataDictKeyDateKeyFloor[day][floor][i-size]
                        else:
                            if prevDay in dataDictKeyDateKeyFloor:
                                pastTS, pastVal = dataDictKeyDateKeyFloor[prevDay][floor][i-size]
                            else:
                                pastTS, pastVal = None, np.mean([val for ts, val in dataDictKeyDateKeyFloor[day][floor]]) # default values for the first day queried, will not affect more than 8 values
                        time = timestamp.time() # may need to format to get rid of milliseconds, or SOMETHING?
                        date = timestamp.date()
                        if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                            continue
                        trajectoryDataKeySizeKeyFloorKeyTS[size][floor][timestamp]=  value - pastVal
        for size in trajectoryDataKeySizeKeyFloorKeyTS):
            self.xListFloorData.append(trajectoryDataKeySizeKeyFloorKeyTS[size])


    def trajectoryCalculatorNoFloor(self, dataDictKeyDate, trajectorySizes):
        maxSpace = np.max(trajectorySizes)
        trajectoryDataKeySizeKeyTS = {}
        for day in dataDictKeyDate:
            prevDay = day+ datetime.timedelta(-1)
            for size in trajectorySizes:
                if size not in trajectoryDataKeySizeKeyTS:
                    trajectoryDataKeySizeKeyTS[size] = {}
                for i in range(0, len(dataDictKeyDate[day])):
                    timestamp, value = dataDictKeyDate[day][i]
                    if i >= size:
                        pastTS, pastVal = dataDictKeyDate[day][i-size]
                    else:
                        if prevDay in dataDictKeyDate:
                            pastTS, pastVal = dataDictKeyDate[prevDay][i-size]
                        else:
                            pastTS, pastVal = 0, np.mean([val for ts, val in dataDictKeyDate[day]]) # default values for the first day queried, will not affect more than 8 values
                    time = timestamp.time() # may need to format to get rid of milliseconds, or SOMETHING?
                    date = timestamp.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        continue
                    trajectoryDataKeySizeKeyTS[size][timestamp]=  value - pastVal
        for size in trajectoryDataKeySizeKeyTS):
            self.xListNoFloorData.append(trajectoryDataKeySizeKeyTS[size])


    def generateTimeData(self):
        if len(self.trajectoryListNoFloorData) == 0:
            print "Please run Trajectory Calculator to generate all trajectory values before running this function"
            return
        timeData = {}
        maxSpace = np.max(self.trajectorySizes)
        trajectoryItem = self.trajectoryListNoFloorData[0]
        for timestamp in trajectoryItem[maxSpace]:
            timeData[timestamp] = timestamp.hour * 60 + timestamp.minute
        self.xListNoFloorData.append(timeData)


    def generateSinglePointDataFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            for floor in dataDictKeyDateKeyFloor[day]:
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    time = ts.time()
                    date = ts.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        continue
                    singlePointDataKeyFloorKeyTS[floor][ts] = value
        self.xListFloorData.append(singlePointDataKeyFloorKeyTS)


    def generateSinglePointDataNoFloor(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            for ts, value in dataDictKeyDate[day]:
                time = ts.time()
                date = ts.date()
                if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                    continue
                singlePointDataKeyTS[ts] = value
        self.xListNoFloorData.append(singlePointDataKeyTS)


    def generateCumulativeValueFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            for floor in dataDictKeyDateKeyFloor[day]:
                runningSum = 0
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    runningSum += value
                    time = ts.time()
                    date = ts.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        continue
                    singlePointDataKeyFloorKeyTS[floor][ts] = runningSum
        self.xListFloorData.append(singlePointDataKeyFloorKeyTS)


    def generateCumulativeValueNoFloor(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            runningSum = 0
            for ts, value in dataDictKeyDate[day]:
                runningSum += value
                time = ts.time()
                date = ts.date()
                if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                    continue
                singlePointDataKeyTS[ts] = runningSum
        self.xListNoFloorData.append(singlePointDataKeyTS)

    def generatePercentageOfMaxNoFloor(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            runningMax = -np.inf
            for ts, value in dataDictKeyDate[day]:
                if runningMax < value:
                    runningMax = value
                percentage = value/runningMax
                time = ts.time()
                date = ts.date()
                if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                    continue
                singlePointDataKeyTS[ts] = percentage
        self.xListNoFloorData.append(singlePointDataKeyTS)

    def generatePercentageOfMaxFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        for day in dataDictKeyDate:
            for floor in self.paramObj.floorList:
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                runningMax = -np.inf
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    if runningMax < value:
                        runningMax = value
                    percentage = value/runningMax
                    time = ts.time()
                    date = ts.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        continue
                    singlePointDataKeyFloorKeyTS[floor][ts] = percentage
        self.xListFloorData.append(singlePointDataKeyTS) 


    def generateOutputData(self):
        pass

    '''
    Matrix Preparation Functions
    ____________________________
    '''


    def queryMatrixOrganizer(self):
        maxSpace = np.max(self.trajectorySizes)
        # Here, we use single point data generated for the prediction date to determine the size of our matrix
        mCount = 0
        self.tsList = []
        for ts in self.xListNoFloorData[0]:
            if ts.day == self.startDatetime.day:
                mCount +=1
                self.tsList.append(ts)
        self.tsList.sort()
        self.queryM = mCount
        self.xQueryMatrix = np.zeros((self.queryM, self.n))
        '''
        In a similar fashion to how the matrix data was generated for the training matrices
        we now generate similar test matrices
        '''
        '''
        First we populate the x query matrix with data in variables "*FloorData"
        '''
        rowCount = 0
        for ts in self.tsList:
            if rowCount > self.queryM:
                print "query matrix malformed: more rows seen than expected"
                break
            colCount = 0
            for floor in self.paramObj.floorList:    
                for trajectories in self.trajectoryListFloorData:
                    for size in self.trajectorySizes:
                        if ts in trajectories[size][floor]:
                            self.xQueryMatrix[rowCount, colCount] = trajectories[size][floor][ts]
                            colCount = colCount + 1
                        else:
                            self.xQueryMatrix[rowCount, colCount] = 0.0001
                            print "query matrix malformed: timestamp value " + str(ts) + " not found in trajectories floor data "
                            colCount = colCount + 1
            for floor in self.paramObj.floorList:
                for data in self.xListFloorData:
                    if ts in data[floor]:
                        self.xQueryMatrix[rowCount, colCount] = data[floor][ts]
                        colCount = colCount + 1
                    else:
                        self.xQueryMatrix[rowCount, colCount] = 0.0001
                        print "query matrix malformed: timestamp value " + str(ts) + " not found in xList floor data "
                        colCount = colCount + 1
            '''
            next we look at data without floor values
            '''
            for trajectories in self.trajectoryListNoFloorData:
                for size in self.trajectorySizes:
                    if ts in trajectories[size]:
                        self.xQueryMatrix[rowCount, colCount] = trajectories[size][ts]
                        colCount = colCount + 1
                    else:
                        self.xQueryMatrix[rowCount, colCount] = 0.0001
                        print "query matrix malformed: timestamp value " + str(ts) + " not found in trajectories no floors"
                        colCount = colCount + 1
            for data in self.xListNoFloorData:
                if ts in data:
                    self.xQueryMatrix[rowCount, colCount] = data[ts]
                    colCount = colCount + 1
                else:
                    self.xQueryMatrix[rowCount, colCount] = 0.0001
                    print "query matrix malformed: timestamp value " + str(ts) + " not found in xList no floors"
                    colCount = colCount + 1
            rowCount = rowCount + 1
        

    def matrixOrganizer(self):
        maxSpace = np.max(self.trajectorySizes)
        # because the values for the output are most prone to having less timestamp elements than the rest, we design our input/output matrices around it
        self.m = len(self.yLabels)
        numberOfFloors = len(self.paramObj.floorList)
        numberOfSizes = len(self.trajectorySizes)
        self.n = len(self.trajectoryListFloorData) * numberOfFloors * numberOfSizes
        self.n+= len(self.trajectoryListNoFloorData) * numberOfSizes
        self.n += len(self.xListFloorData) *numberOfFloors
        self.n += len(self.xListNoFloorData)
        self.xMatrices = np.zeros((self.m, self.n))
        self.yMatrices = np.zeros(self.m)
        '''
        We wish to create a grand X matrix with many parameters.  
        '''
        '''
        First we populate the x matrix with data in variables "*FloorData"
        '''
        rowCount = 0
        for ts in self.yLabels:
            if rowCount > self.m:
                print "uneven length in yList per floor, breaking matrix assigment loop"
                break
            colCount = 0
            for floor in self.paramObj.floorList:    
                for trajectories in self.trajectoryListFloorData:
                    for size in self.trajectorySizes:
                        if ts in trajectories[size][floor]:
                            self.xMatrices[rowCount, colCount] = trajectories[size][floor][ts]
                            colCount = colCount + 1
                        else:
                            self.xMatrices[rowCount, colCount] = 0.0001
                            print "timestamp value " + str(ts) + " not found in trajectories floor data "
                            colCount = colCount + 1
            for floor in self.paramObj.floorList:
                for data in self.xListFloorData:
                    if ts in data[floor]:
                        self.xMatrices[rowCount, colCount] = data[floor][ts]
                        colCount = colCount + 1
                    else:
                        self.xMatrices[rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in xList floor data "
                        colCount = colCount + 1
            '''

            next we look at data without floor values
            '''
            for trajectories in self.trajectoryListNoFloorData:
                for size in self.trajectorySizes:
                    if ts in trajectories[size]:
                        self.xMatrices[rowCount, colCount] = trajectories[size][ts]
                        colCount = colCount + 1
                    else:
                        self.xMatrices[rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in trajectories no floors"
                        colCount = colCount + 1
            for data in self.xListNoFloorData:
                if ts in data:
                    self.xMatrices[rowCount, colCount] = data[ts]
                    colCount = colCount + 1
                else:
                    self.xMatrices[rowCount, colCount] = 0.0001
                    print "timestamp value " + str(ts) + " not found in xList no floors"
                    colCount = colCount + 1
            if ts in self.yLabels:
                self.yMatrices[rowCount] = self.yLabels[ts]
            else:
                self.yMatrices[rowCount] = 0.0001
                print "timestamp value  " + str(ts) + " not found for output"
            rowCount = rowCount + 1


    def scaleData(self):
        self.scaler = preprocessing.StandardScaler().fit(self.xMatrices)
        self.xMatrices = self.scaler.transform(self.xMatrices)
