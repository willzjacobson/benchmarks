from data_tools.dataCollectors import *
import random
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import pylab as pl
import pyodbc
from sklearn import preprocessing
from sklearn.linear_model import LassoCV
from sklearn.svm import SVC as SVM
from sklearn import grid_search
import cPickle as pickle

'''
this module provides a generalistic framework for implementing an SVM classifier
as a change point detector.

Each instantiation should declare the functions readFromDB(), generateCovariates(),
commitFinalPredictions() and borrowData() (if applicable)

The output labels generator function accepts a "rawDataKeyDay" dictionary
which holds the time of day during which the transition occurs.  All points
before the transition are labeled 0 -- all points after are labeled 1.

We look for the transition from 0 to 1 -- the decision boundary
'''

class changePointSVMBase():
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        #self.lgr= lgr
        #self.options = options
        self.conn = conn
        self.cursor = cursor
        self.paramObj = paramObj
        self.runDatetime = datetime.datetime.now()
        self.performGridSearch = performGridSearch
        self.startDatetime = startDatetime
        self.relevantHoursTuple = relevantHoursTuple
        self.trajectorySizes = trajectorySizes
        self.numberOfDays = numberOfDays
        self.trajectoryListNoFloorData = []
        self.trajectoryListFloorData = []
        self.xListFloorData = []
        self.xListNoFloorData = []
        self.yLabels = None
        self.xMatrices = None
        self.yMatrices = None
        self.scaler = None
        self.gridSearchObjects = None
        self.bestSVM = None
        self.optimalParameters = None
        self.xqueryMatrix = None
        self.m = None
        self.n = None
        self.tsList= None
        self.finalPredictions = None
        self.interpolatedQueryMatrix = None
        self.transitionTime = None
        self.interpolatedPreditions = None
        self.finalPrediction = None

    def readFromDB(self):
        pass

    def generateCovariates(self):
        pass

    

    def autorun(self):
        self.generateCovariates()
        # place into matrices
	self.matrixOrganizer()
        print "data and label matrices constructed..."
        
        # scale data
        self.scaleData()
        print "data scaled"

        # perform grid search and train SVM, or load parameters and train SVM
        if self.performGridSearch == False:
            print "loading parameters and training SVM..."
            self.getParameters()
        else:
            print "performing grid search and writing parameters..."
            self.SVMGridSearch(5)

        # generate test matrix
        self.queryMatrixOrganizer()
        print "test matrix constructed.  Running final predictions..."

        self.predictQueryMatrix()
        counter = 0
        print self.startDatetime
        print self.tsList
        for ts in self.tsList:
            print str(ts) + ": " + str(self.finalPredictions[counter])
            counter+= 1

        self.createInterpolatedQuery()
        self.predictInterpolatedQuery()
        self.generateFinalPredictionTime()
        print "interpolated query constructed and predicted upon..."
        print self.startDatetime
        for k in range(16):
            print str(self.transitionTime + datetime.timedelta(0,k*60)) + ": " + str(self.interpolatedPredictions[k])

        print "final time: " + str(self.finalPrediction)

        


    '''
    Data Generation Functions
    _________________________
    '''
        

    def generateChangeDataFloorData(self, dataDictKeyDateKeyFloor):
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


    def generateChangeDataNoFloor(self, dataDictKeyDate):
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
        


    def trajectoryCalculatorFloorData(self, dataDictKeyDateKeyFloor):
        maxSpace = np.max(self.trajectorySizes)
        trajectoryDataKeySizeKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            prevDay = day+ datetime.timedelta(-1)
            for size in self.trajectorySizes:
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
        self.trajectoryListFloorData.append(trajectoryDataKeySizeKeyFloorKeyTS)


    def trajectoryCalculatorNoFloor(self, dataDictKeyDate):
        maxSpace = np.max(self.trajectorySizes)
        trajectoryDataKeySizeKeyTS = {}
        for day in dataDictKeyDate:
            prevDay = day+ datetime.timedelta(-1)
            for size in self.trajectorySizes:
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
        self.trajectoryListNoFloorData.append(trajectoryDataKeySizeKeyTS)


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


    def generateOutputData(self, outputDictKeyDate):
        self.yLabels = {}
        if len(self.trajectoryListNoFloorData) == 0:
            print "Please run Trajectory Calculator to generate all trajectory values before running this function"
            return
        labelData = {}
        maxSpace = np.max(self.trajectorySizes)
        trajectoryItem = self.trajectoryListNoFloorData[0]
        startupTimes = {}
        for timestamp in trajectoryItem[maxSpace]:
            if timestamp.date() not in startupTimes:
                if timestamp.date() != self.startDatetime.date():
                    startupTimes[timestamp.date()] = outputDictKeyDate[timestamp.date()]
                    date = timestamp.date()
                    #print "startup time for " + str(date) +": " + str(outputDictKeyDate[date])
            if timestamp.date() == self.startDatetime.date():
                continue
            
            labelData[timestamp] = 1*(timestamp > outputDictKeyDate[timestamp.date()])
        self.yLabels = labelData

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

    def createInterpolatedQuery(self):
        self.interpolatedQueryMatrix = np.zeros((16, self.n))
        zero_oneTransition = None
        numOnesInRow = {}
        oneFlag = False
        for n in range(len(self.finalPredictions) -1):
            if int(self.finalPredictions[n]) == 0 and int(self.finalPredictions[n+1]) == 1:
                zero_oneTransition = n
                oneFlag = True
                if n not in numOnesInRow:
                    numOnesInRow[zero_oneTransition] = 0
            elif oneFlag == True and int(self.finalPredictions[n]) == 1:
                numOnesInRow[zero_oneTransition] += 1
            elif int(self.finalPredictions[n]) == 0:
                oneFlag = False
            elif int(self.finalPredictions[n]) == 1 and oneFlag == False:
                #handles the case when the first value is 1
                oneFlag = True
                zero_oneTransition = n
                numOnesInRow[zero_oneTransition] = 1
        maxOnes = 0
        maxN = None
        for zero_one in numOnesInRow:
            numOnes = numOnesInRow[zero_one]
            if numOnes > maxOnes:
                maxOnes = numOnes
                maxN = zero_one
        zero_oneTransition = maxN
        for k in range(self.n):
            dummyArray = np.zeros(16)
            dummyArray[0] = self.xQueryMatrix[zero_oneTransition, k]
            dummyArray[15] = self.xQueryMatrix[zero_oneTransition +1, k]
            if np.isnan(dummyArray[0]):
                dummyArray[0] = 0
            if np.isnan(dummyArray[15]):
                dummyArray[15] = 0
            dummyArray[1:15:1] = np.nan
            not_nan = np.logical_not(np.isnan(dummyArray))
            indices = np.arange(16)
            dummyArray = np.interp(indices,[0,15], [dummyArray[0],dummyArray[15]])
            self.interpolatedQueryMatrix[::1, k] = dummyArray
        self.transitionTime = self.tsList[zero_oneTransition]

    def generateFinalPredictionTime(self):
        for k in range(len(self.interpolatedPredictions)):
            if int(self.interpolatedPredictions[k]) == 0 and int(self.interpolatedPredictions[k+1]) ==1:
                self.finalPrediction = self.transitionTime + datetime.timedelta(0,60*(k+1))


    '''
    SVM Training/Test Functions
    ___________________________
    '''


    def predictQueryMatrix(self):
        self.finalPredictions = None
        scaledQueryMatrix = self.scaler.transform(self.xQueryMatrix)
        self.finalPredictions = self.bestSVM.predict(scaledQueryMatrix)

    def predictInterpolatedQuery(self):
        self.interpolatedPredictions = None
        scaledInterpolatedQuery = self.scaler.transform(self.interpolatedQueryMatrix)
        self.interpolatedPredictions = self.bestSVM.predict(scaledInterpolatedQuery)

    def SVMGridSearch(self, numberOfFolds):
        self.gridSearchObjects = {}
        self.bestSVM = None
        parameters = {'kernel': ['rbf'], 'gamma': [1, 1e-1, 1e-2, 1e-3, 1e-4],
                     'C': [.01, .1, 1, 10, 100, 1000]}
        predictor = SVM()
        self.gridSearchObjects = grid_search.GridSearchCV(predictor, parameters, cv = numberOfFolds)
        self.bestSVM = self.gridSearchObjects.fit(self.xMatrices, self.yMatrices)
        self.writeParameters()


    def writeParameters(self):
        filename = "SVM_parameters.p"
        outfile = open(filename, 'wb')
        self.optimalParameters = None
        self.optimalParameters = self.gridSearchObjects.best_params_
        pickle.dump(self.optimalParameters, outfile)
        outfile.close()


    def getParameters(self):
        filename = "SVM_parameters.p"
        infile = open(filename, 'rb')
        self.optimalParameters = pickle.load(infile)
        infile.close()
        self.bestSVM = None
        optParams = self.optimalParameters
        self.bestSVM = SVM(kernel = optParams['kernel'], C = optParams['C'], gamma = optParams['gamma'])
        self.bestSVM = self.bestSVM.fit(self.xMatrices, self.yMatrices)


    '''
    SQL commit functions
    ____________________
    '''

    def commitFinalPediction(self,tableName):
        pass



	


                                                            
