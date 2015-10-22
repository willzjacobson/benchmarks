from data_tools.dataCollectors import *
import random
#import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
#import pylab as pl
import pyodbc
from sklearn import preprocessing
from sklearn.linear_model import LassoCV
from sklearn.svm import SVR
from sklearn import grid_search
import cPickle as pickle



class trajectoryPredictorBase():
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime, predictionTimestep, performGridSearch, trajectorySizes, relevantHoursTuple):
        # set attribute values
        self.conn = conn
        self.cursor = cursor
        self.paramObj = paramObj
        self.predictionTimestep = predictionTimestep
        self.performGridSearch = performGridSearch
        self.startDatetime = startDatetime
        self.relevantHoursTuple = relevantHoursTuple
        self.trajectorySizes = trajectorySizes
        self.numberOfDays = numberOfDays
        self.startDatetime = startDatetime
        self.runDatetime = datetime.datetime.now()
        self.trajectoryList = []
        self.xList = []
        self.yList = None
        self.xMatrices = None
        self.yMatrices = None
        self.scaler = None
        self.gridSearchObjects = None
        self.bestSVR = None
        self.optimalParameters = None
        self.queryVector = None
        self.m = None
        self.n = None
        self.maxTS = None
        self.finalSptPredictions = None
        
    def readFromDB(self):
        pass

    def borrowData(self):
        pass

    def generateCovariates(self):
        pass


    def autorun(self):
        self.generateCovariates()
        # Place into Matrices
        print "formatting into matrix form..."
        self.matrixOrganizer()
        print "scaling data..."
        # generate Scaler and Scale Data
        self.scaleData()
        
        if self.performGridSearch == False:
            print "loading parameters and training SVR..."
            self.getParameters()
        else:
            print "performing grid search..."
            self.SVRGridSearch(5)

        self.makeQueryVector()
            
        self.predictQueryVector()

        print self.maxTS
        for floor in self.finalSptPredictions:
            print str(floor) + ": " + str(self.finalSptPredictions[floor][0])

    def commitPredictionsSQL(self):
        pass
        
            
            
    def writePredictions(self, filename, writeOrAppend = 'a'):
        outfile = open(filename, writeOrAppend)
        if writeOrAppend == 'w':
            counter = 0
            floorLength = len(self.paramObj.floorList)
            for floor in self.paramObj.floorList:
                counter = counter + 1
                outfile.write(str(floor))
                if counter < floorLength:
                    outfile.write(',')
                else:
                    outfile.write('\n')
        counter = 0
        floorLength = len(self.paramObj.floorList)
        for floor in self.paramObj.floorList:
            counter = counter + 1
            outfile.write(str(self.finalSptPredictions[floor][0]))
            if counter < floorLength:
                outfile.write(',')
            else:
                outfile.write('\n')

    def scaleData(self):
        self.scaler = {}
        for floor in self.xMatrices:
            self.scaler[floor] = preprocessing.StandardScaler().fit(self.xMatrices[floor])
            self.xMatrices[floor] = self.scaler[floor].transform(self.xMatrices[floor])

    def predictQueryVector(self):
        self.finalSptPredictions = {}
        for floor in self.paramObj.floorList:
            scaledQueryVector = self.scaler[floor].transform(self.queryVector[floor])
            #print "Query Vector for floor " + str(floor)
            #print self.queryVector[floor]
            #print "scaled query vector:"
            #print scaledQueryVector
            self.finalSptPredictions[floor] = self.bestSVR[floor].predict(scaledQueryVector)

    def makeQueryVector(self):
        self.queryVector = {}
        self.maxTS = self.SptDataCollector.maxTS
        for floor in self.paramObj.floorList:
            self.queryVector[floor]=np.zeros(self.n)
            colCount= 0
            for trajectories in self.trajectoryList:
                for size in self.trajectorySizes:
                    if self.maxTS in trajectories[size][floor]:
                        self.queryVector[floor][colCount] = trajectories[size][floor][self.maxTS]
                        colCount = colCount + 1
                    else:
                        self.queryVector[floor][colCount] = 0.0001
                        print "timestamp value " + str(self.maxTS) + " not found in trajectories "
                        print "query Vector malformed"
                        colCount = colCount + 1
            for data in self.xList:
                if self.maxTS in data[floor]:
                    self.queryVector[floor][colCount] = data[floor][self.maxTS]
                    colCount = colCount + 1
                else:
                    self.queryVector[floor][colCount] = 0.0001
                    print "timestamp value " + str(self.maxTS) + " not found in xList "
                    print "query Vector malformed"
                    colCount = colCount + 1
        
            

    def SVRGridSearch(self, numberOfFolds):
        self.gridSearchObjects = {}
        self.bestSVR = {}
        parameters = {'kernel': ['rbf'], 'gamma': [1, 1e-1, 1e-2, 1e-3, 1e-4],
                     'C': [.01, .1, 1, 10, 100, 1000]}
        for floor in self.paramObj.floorList:
            predictor = SVR()
            print "grid search for floor: " + str(floor)
            self.gridSearchObjects[floor] = grid_search.GridSearchCV(predictor, parameters, cv = numberOfFolds)
            self.bestSVR[floor] = self.gridSearchObjects[floor].fit(self.xMatrices[floor], self.yMatrices[floor])

        self.writeParameters()

    def writeParameters(self):
        filename = "SVR_parameters_" +str(self.predictionTimestep) + ".p"
        outfile = open(self.paramObj.sptTrajectoryParams.paramSavepoint+ '\\' + filename, 'wb')
        self.optimalParameters = {}
        for floor in self.gridSearchObjects:
            self.optimalParameters[floor] = self.gridSearchObjects[floor].best_params_
        pickle.dump(self.optimalParameters, outfile)
        outfile.close()

    def getParameters(self):
        filename = "SVR_parameters_" +str(self.predictionTimestep) + ".p"
        infile = open(self.paramObj.sptTrajectoryParams.paramSavepoint+ '\\' + filename, 'rb')
        self.optimalParameters = pickle.load(infile)
        #print self.optimalParameters
        infile.close()
        self.bestSVR = {}
        for floor in self.paramObj.floorList:
            #print filename
            optParams = self.optimalParameters[floor]
            self.bestSVR[floor] = SVR(kernel = optParams['kernel'], C = optParams['C'], gamma = optParams['gamma'])
            self.bestSVR[floor] = self.bestSVR[floor].fit(self.xMatrices[floor], self.yMatrices[floor])
            

    def matrixOrganizer(self):
        maxSpace = np.max(self.trajectorySizes)
        # because the values for the output are most prone to having less timestamp elements than the rest, we design our input/output matrices around it
        someFloor = None
        for floors in self.trajectoryList[1][maxSpace]:
            someFloor = floors
            break
        self.n = len(self.trajectoryList) * len(self.trajectorySizes) + len(self.xList)
        self.m = {}#len(self.yList[someFloor])
        self.validTS = {}
        for floor in self.paramObj.floorList:
            self.m[floor] = 0
            self.validTS[floor] = []
            for ts in self.yList[floor]:
                flag = 0
                for trajectories in self.trajectoryList:
                    for size in self.trajectorySizes:
                        if ts not in trajectories[size][floor]:
                            flag +=1
                for data in self.xList:
                    if ts not in data[floor]:
                        flag+=1
                if flag != 0:
                    continue
                    
                self.m[floor]+=1
                self.validTS[floor].append(ts)
            
                
        self.xMatrices = {}
        self.yMatrices = {}
        for floor in self.paramObj.floorList:
            if floor not in self.xMatrices:
                self.xMatrices[floor] = np.zeros((self.m[floor], self.n))
            if floor not in self.yMatrices:
                self.yMatrices[floor] = np.zeros(self.m[floor])
            rowCount = 0
            for ts in self.validTS[floor]:
                colCount = 0
                for trajectories in self.trajectoryList:
                    for size in self.trajectorySizes:
                        if ts in trajectories[size][floor]:
                            self.xMatrices[floor][rowCount, colCount] = trajectories[size][floor][ts]
                            colCount = colCount + 1
                        else:
                            self.xMatrices[floor][rowCount, colCount] = self.xMatrices[floor][rowCount-1, colCount]
                            print "timestamp value " + str(ts) + " not found in trajectories "
                            colCount = colCount + 1
                for data in self.xList:
                    if ts in data[floor]:
                        self.xMatrices[floor][rowCount, colCount] = data[floor][ts]
                        colCount = colCount + 1
                    else:
                        self.xMatrices[floor][rowCount, colCount] = 0.0001
                        print "timestamp value " + str(ts) + " not found in xList"
                        colCount = colCount + 1
                if ts in self.yList[floor]:
                    self.yMatrices[floor][rowCount] = self.yList[floor][ts]
                else:
                    self.yMatrices[floor][rowCount] = 0.0001
                    print "timestamp value not found for output"
                rowCount = rowCount + 1
                if rowCount > self.m:
                    print "uneven length in yList per floor, breaking matrix assigment loop"
                    break
                    
                
            

    def trajectoryCalculator(self, dataDictKeyDateKeyFloor):
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
                                try:
                                    pastTS, pastVal = dataDictKeyDateKeyFloor[prevDay][floor][i-size]
                                except:
                                    pastTS, pastVal = 0, 73     
                            else:
                                pastTS, pastVal = 0, 73
                        time = timestamp.time() # may need to format to get rid of milliseconds, or SOMETHING?
                        date = timestamp.date()
                        if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                            continue
                        trajectoryDataKeySizeKeyFloorKeyTS[size][floor][timestamp]=  value - pastVal
        self.trajectoryList.append(trajectoryDataKeySizeKeyFloorKeyTS)

    def generateHourData(self):
        if len(self.trajectoryList) == 0:
            print "Please run Trajectory Calculator to generate all trajectory values before running this function"
            return
        hourData = {}
        maxSpace = np.max(self.trajectorySizes)
        trajectoryItem = self.trajectoryList[1]
        for floor in self.paramObj.floorList:
            if floor not in hourData:
                hourData[floor] = {}
            for timestamp in trajectoryItem[maxSpace][floor]:
                hourData[floor][timestamp] = timestamp.hour
        self.xList.append(hourData)

    def generateSinglePointData(self, dataDictKeyDateKeyFloor):
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
        self.xList.append(singlePointDataKeyFloorKeyTS)

    def generateOutputData(self, outputDataDictKeyDateKeyFloor):
        outputDataKeyFloorKeyTS = {}
        for day in outputDataDictKeyDateKeyFloor:
            for floor in outputDataDictKeyDateKeyFloor[day]:
                if floor not in outputDataKeyFloorKeyTS:
                    outputDataKeyFloorKeyTS[floor] = {}
                for n in range(0, len(outputDataDictKeyDateKeyFloor[day][floor]) - self.predictionTimestep):
                    ts, value = outputDataDictKeyDateKeyFloor[day][floor][n]
                    futureTS, futureVal = outputDataDictKeyDateKeyFloor[day][floor][n + self.predictionTimestep]
                    time = ts.time()
                    date = ts.date()
                    if time < self.relevantHoursTuple[0] or time > self.relevantHoursTuple[1]:
                        continue
                    outputDataKeyFloorKeyTS[floor][ts] = futureVal
        self.yList = outputDataKeyFloorKeyTS
        
        
        
                        



        
