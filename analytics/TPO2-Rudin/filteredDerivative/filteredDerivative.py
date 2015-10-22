'''
File containing library to read in prediction data, and create filtered
derivative output.



Hyperparameters:

cursor: instantiate a pyodbc cursor object, and establish a connection with your desired DB server, before creating any class
from this library.  Note that this implementation assumes the prediction data table is:  'Space Temperature Prediction'

windowSize: What window sizes should we test over? defaults to (5, 19), testing over range(5, 19+2, 2)

derivSpace: What derivative spacing should we use? defaults to (4, 12), testing over range(4, 12+2, 2)

contiguousVals: How many contiguous values are required to form a significant event representing a floor's reccomendation

valueTable: contains the entries in the database for the true rampdown (or ramp up, for later analysis); defaults to 'Ramp_Down_time_DS'

includeWeekends: should we include weekends in our analysis? defaults to False

lookForNegs: Should we be looking for contiguous sequences of negative derivatives? defaults to True. Use False if you are looking for positive derivatives

FDtimeTuple: a tuple of times for the filtered Derivative to analyze;  defaults to (timedate.time(12,30), timedate.time(19,00)) for rampdown, and to (3:45AM, 7:30 AM) for rampup



'''

import random
import matplotlib.pyplot as plt
import datetime 
import numpy
import math
import pylab as pl
from sklearn.linear_model import LassoCV

class FilteredDerivativeBase():
    def __init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate = None, windowSize = (5, 19), derivSpace = (4,12), contiguousVals = (5,7), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        self.timeStamp = datetime.datetime.now()
        self.valueTable = valueTable
        self.conn = conn
        self.cursor = cursor
        self.predictionDataTable = {}
        self.trueValTableKeyDate = {}
        self.floorList = floorList
        self.train_start_date = train_start_date
        self.train_end_date = train_end_date
        self.test_start_date = test_start_date
        self.test_end_date = test_end_date
        self.windowSizeTuple = windowSize
        self.derivSpaceTuple = derivSpace
        self.contiguousVals = contiguousVals
        self.finalPredictionDate = finalPredictionDate
        self.fdtrainer_fdtester = {}
        self.includeWeekends = includeWeekends
        self.lookForNegs = lookForNegs
        self.predictedVal = None
        self.minTup = None
        self.FDtimeTuple = FDtimeTuple
        
        self.populateDataTables()

        for window in range(windowSize[0], windowSize[1] +2, 2):
            for deriv in range(derivSpace[0], derivSpace[1] +2, 2):
                for contiguous in range(contiguousVals[0], contiguousVals[1] +1 ,1):
                    trainer = FilteredDerivativeTrainer(self.predictionDataTable, self.trueValTableKeyDate, self.train_start_date, self.train_end_date, self.floorList, window, deriv, contiguous, self.includeWeekends, self.lookForNegs, self.FDtimeTuple)
                    trainer.fillRegressionWeights()
                    tester = FilteredDerivativeTester(self.predictionDataTable, self.trueValTableKeyDate, self.test_start_date, self.test_end_date, self.floorList, window, deriv, contiguous, self.includeWeekends,self.lookForNegs, self.FDtimeTuple)
                    tester.calculatePredictions(trainer.regressionObject)
                    self.fdtrainer_fdtester[(window, deriv, contiguous)] = (trainer, tester)
        minError = numpy.inf
        for tup in self.fdtrainer_fdtester:
            if self.fdtrainer_fdtester[tup][1].squaredError < minError:
                minError = self.fdtrainer_fdtester[tup][1].squaredError
                self.minTup = tup
                print "minTup " + str(self.minTup)
            print tup, self.fdtrainer_fdtester[tup][1].squaredError
        if self.finalPredictionDate != None:
            self.predictedVal = self.fdtrainer_fdtester[self.minTup][1].predict(self.fdtrainer_fdtester[self.minTup][0].regressionObject, self.finalPredictionDate, False)


    def populateDataTables(self):
        self.populateWithDates(self.train_start_date, self.train_end_date)
        self.populateWithDates(self.test_start_date, self.test_end_date)
        if self.finalPredictionDate != None:
            self.populateWithDates(self.finalPredictionDate, self.finalPredictionDate, False)

               
    
    def populateWithDates(self, start_date, end_date, setValueTable = True):
        pass

    def predictDate(self, predictionDate, plot = False):
        if predictionDate not in self.predictionDataTable:
            self.populateWithDates(predictionDate, predictionDate, setValueTable = False)
        return self.fdtrainer_fdtester[self.minTup][1].predict(self.fdtrainer_fdtester[self.minTup][0].regressionObject, predictionDate, plot)

    def plotTruthAndPrediction(self, numberOfPlots = 1):
        minTester = self.fdtrainer_fdtester[self.minTup][1]
        minTrainer = self.fdtrainer_fdtester[self.minTup][0]
        if numberOfPlots > len(minTester.filteredDerivsKeyDay):
            numberOfPlots = len(minTester.filteredDerivsKeyDay)
        perm = [key for key in minTester.filteredDerivsKeyDay]
        random.shuffle(perm, random=random.random)
        perm = perm[0:numberOfPlots]
        for key in perm:
            minTester.filteredDerivsKeyDay[key].plot(True,False,True, minTester.predict(minTrainer.regressionObject, key, False))


        


    def valQueryFunction(self, day):
        pass

    def commitPredictions_SQL(self, table, start_date, end_date):
        for n in range(int((end_date - start_date).days +1)):
            day = start_date + datetime.timedelta(n)
            if day.weekday() == 6 or day.weekday() == 5:
                if self.includeWeekends == False:
                    continue
            query = "insert into " + table + "(Run_DateTime, Prediction_DateTime) values ('" + self.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + str(self.predictDate(day, False)) +"' )"
            self.cursor.execute(query)
            self.conn.commit()
        print "Committed Predictions"

    def commitTrueVals_SQL(self, table):
        trainer = self.fdtrainer_fdtester[self.minTup][0]
        tester = self.fdtrainer_fdtester[self.minTup][1]
        for day in trainer.filteredDerivsKeyDay:
            if day not in self.trueValTableKeyDate:
                continue
            trueTime = self.trueValTableKeyDate[day]
            trueTime = datetime.datetime.combine(day, trueTime)
            query = "insert into " + table + " (Run_DateTime, Actual_DateTime) values ('" + self.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + trueTime.strftime("%Y-%m-%d %H:%M") + "' )"
            self.cursor.execute(query)
            self.conn.commit()
        for day in tester.filteredDerivsKeyDay:
            if day not in self.trueValTableKeyDate:
                continue
            trueTime = self.trueValTableKeyDate[day]
            trueTime = datetime.datetime.combine(day, trueTime)
            query = "insert into " + table + " (Run_DateTime, Actual_DateTime) values ('" + self.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + trueTime.strftime("%Y-%m-%d %H:%M") + "' )"
            self.cursor.execute(query)
            self.conn.commit()
        print "Committed True Values"

    def commitMinTupFDData_SQL(self, table):
        trainer = self.fdtrainer_fdtester[self.minTup][0]
        tester = self.fdtrainer_fdtester[self.minTup][1]
        for day in trainer.filteredDerivsKeyDay:
            for floor in self.floorList:
                fd = trainer.filteredDerivsKeyDay[day].filteredDerivativeKeyFloor[floor]
                for time_value in fd:
                    query = "insert into " + table + " (Run_DateTime, Min_Tuple, Floor, Value_DateTime, Value) values \
                    ('" + self.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + str(self.minTup) + "' , '" + str(floor) + "', '" + str(time_value[0]) + "', " + str(time_value[1]) +" )"
                    self.cursor.execute(query)
                    self.conn.commit()
        for day in tester.filteredDerivsKeyDay:
            for floor in self.floorList:
                fd = tester.filteredDerivsKeyDay[day].filteredDerivativeKeyFloor[floor]
                for time_value in fd:
                    query = "insert into " + table + " (Run_DateTime, Min_Tuple, Floor, Value_DateTime, Value) values \
                    ('" + self.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + str(self.minTup) + "' , '" + str(floor) + "', '" + str(time_value[0]) + "', " + str(time_value[1]) +" )"
                    self.cursor.execute(query)
                    self.conn.commit()            
        print "Committed FD Data"
                
            
            

class FilteredDerivativeRampdownPark(FilteredDerivativeBase):
    '''
    This is the master class for the analysis, and will be the one to carry out the grid search
    over possible values of windowSize, derivSpace, and contiguousVals.  This accepts training and
    test dates, a final prediction date, the range of parameters to be searched, in tuple form, as well
    as some extra specifics-parameters
    '''

    def __init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate = None, windowSize = (5, 19), derivSpace = (4,12), contiguousVals = (5,8), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        FilteredDerivativeBase.__init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate , windowSize , derivSpace , contiguousVals , valueTable , includeWeekends , lookForNegs, FDtimeTuple)

    def valQueryFunction(self, day):
        strDay = day.strftime("'%Y-%m-%d'")
        query = 'Select a.TIMESTAMP from ' + self.valueTable + ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0 and datediff(month, ' + strDay + ', a.TIMESTAMP) = 0 and datediff(year, ' + strDay + ', a.TIMESTAMP) = 0'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if len(rows) == 0:       
            return datetime.time(18,00)
        val = rows[0][0]
        return val.time()

    def populateWithDates(self, start_date, end_date, setValueTable = True):
        predictionTable = 'Space_Temperature_Prediction'
        for n in range(int((end_date - start_date).days) + 1):
            day = start_date + datetime.timedelta(n)
            strDay = day.strftime("'%Y-%m-%d'")
            if day.weekday() == 6 or day.weekday() == 5:
                if self.includeWeekends == False:
                    continue
            self.predictionDataTable[day] = {}
            for floor in self.floorList:
                query = 'Select a.Prediction_DateTime, a.Prediction_Value \
                FROM ' + predictionTable + " a \
                INNER JOIN (SELECT MAX(c.RUN_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime  \
                FROM " +  predictionTable +  " c \
                WHERE datediff(day, " + strDay + ", c.Prediction_DateTime)=0  and datediff(year, " + strDay + ", c.Prediction_DateTime)=0 and datediff(month, " + strDay + ", c.Prediction_DateTime)=0\
                GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime \
                WHERE datediff(day, " + strDay + ", a.Prediction_DateTime)=0 and datediff(month, " + strDay + ", a.Prediction_DateTime)=0 and  datediff(year, " + strDay + ", a.Prediction_DateTime)=0 and a.Floor = " + str(floor)  + " and a.Run_DateTime=b.RunDateTime \
                Order By a.prediction_DateTime"

                self.cursor.execute(query) 
                Predictions = []
                rows = self.cursor.fetchall()
                for i in range(len(rows)):
                    Predictions.append((rows[i][0], rows[i][1]))
                self.predictionDataTable[day][floor] = Predictions

            if setValueTable == True:
                self.trueValTableKeyDate[day] = self.valQueryFunction(day)


class FilteredDerivativeRampdownLex(FilteredDerivativeBase):


    def populateWithDates(self, start_date, end_date, setValueTable = True):
        predictionTable = 'Space_Temperature_Prediction'
        for n in range(int((end_date - start_date).days) + 1):
            day = start_date + datetime.timedelta(n)
            strDay = day.strftime("'%Y-%m-%d'")
            if day.weekday() == 6 or day.weekday() == 5:
                if self.includeWeekends == False:
                    continue
            self.predictionDataTable[day] = {}
            for floor in self.floorList:
                query = 'Select a.Prediction_DateTime, a.Prediction_Value \
                FROM ' + predictionTable + " a \
                INNER JOIN (SELECT MAX(c.RUN_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime  \
                FROM " +  predictionTable +  " c \
                WHERE datediff(day, " + strDay + ", c.Prediction_DateTime)=0 and datediff(month, " + strDay + ", c.Prediction_DateTime)=0 and datediff(year, " + strDay + ", c.Prediction_DateTime)=0\
                GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime \
                WHERE datediff(day, " + strDay + ", a.Prediction_DateTime)=0 and datediff(month, " + strDay + ", a.Prediction_DateTime)=0 and datediff(year, " + strDay + ", a.Prediction_DateTime)=0 and a.Quadrant = '" + floor  + "' and a.Run_DateTime=b.RunDateTime \
                Order By a.prediction_DateTime ASC"

                self.cursor.execute(query) 
                Predictions = []
                rows = self.cursor.fetchall()
                for i in range(len(rows)):
                    Predictions.append((rows[i][0], rows[i][1]))
                self.predictionDataTable[day][floor] = Predictions

            if setValueTable == True:
                self.trueValTableKeyDate[day] = self.valQueryFunction(day)

    def __init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate = None, windowSize = (5, 19), derivSpace = (4,12), contiguousVals = (5,8), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        FilteredDerivativeBase.__init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate , windowSize , derivSpace , contiguousVals , valueTable , includeWeekends , lookForNegs, FDtimeTuple)

    def valQueryFunction(self, day):
        strDay = day.strftime("'%Y-%m-%d'")
        query = 'Select a.TIMESTAMP from ' + self.valueTable + ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0 and datediff(month, ' + strDay + ', a.TIMESTAMP) = 0 and datediff(year, ' + strDay + ', a.TIMESTAMP) = 0'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if len(rows) == 0:       
            return datetime.time(18,00)
        val = rows[0][0]
        return val.time()
        
class FilteredDerivativeStartupPark(FilteredDerivativeBase):
    '''
    This is the master class for the analysis, and will be the one to carry out the grid search
    over possible values of windowSize, derivSpace, and contiguousVals.  This accepts training and
    test dates, a final prediction date, the range of parameters to be searched, in tuple form, as well
    as some extra specifics-parameters
    '''

    def __init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate = None, windowSize = (1, 7), derivSpace = (2,8), contiguousVals = (1,4), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = False, FDtimeTuple = (datetime.time(3,45), datetime.time(7,15))):
        FilteredDerivativeBase.__init__(self,conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate , windowSize , derivSpace , contiguousVals , valueTable , includeWeekends , lookForNegs, FDtimeTuple)


    def populateWithDates(self, start_date, end_date, setValueTable = True):
        predictionTable = 'Space_Temperature_Prediction'
        for n in range(int((end_date - start_date).days) + 1):
            day = start_date + datetime.timedelta(n)
            strDay = day.strftime("'%Y-%m-%d'")
            if day.weekday() == 6 or day.weekday() == 5:
                if self.includeWeekends == False:
                    continue
            self.predictionDataTable[day] = {}
            for floor in self.floorList:
                query = 'Select a.Prediction_DateTime, a.Prediction_Value \
                FROM ' + predictionTable + " a \
                INNER JOIN (SELECT MAX(c.RUN_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime  \
                FROM " +  predictionTable +  " c \
                WHERE datediff(day, " + strDay + ", c.Prediction_DateTime)=0 and  datediff(month, " + strDay + ", c.Prediction_DateTime)=0 and  datediff(year, " + strDay + ", c.Prediction_DateTime)=0\
                GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime \
                WHERE datediff(day, " + strDay + ", a.Prediction_DateTime)=0 and  datediff(month, " + strDay + ", a.Prediction_DateTime)=0 and  datediff(year, " + strDay + ", a.Prediction_DateTime)=0and a.Floor = " + str(floor)  + " and a.Run_DateTime=b.RunDateTime \
                Order By a.prediction_DateTime"

                self.cursor.execute(query) 
                Predictions = []
                rows = self.cursor.fetchall()
                for i in range(len(rows)):
                    Predictions.append((rows[i][0], rows[i][1]))
                self.predictionDataTable[day][floor] = Predictions

            if setValueTable == True:
                self.trueValTableKeyDate[day] = self.valQueryFunction(day)

    def valQueryFunction(self,day):
        strDay = day.strftime("'%Y-%m-%d'")
        lowBound = datetime.datetime.combine(day, datetime.time(03,45))
        upperBound = datetime.datetime.combine(day, datetime.time(07,15))
        trueValsTemp = {}
        fansOn = 0
        val = None
        for tableName in self.valueTable:

            trueValsTemp[tableName] = None
            query = 'Select a.TIMESTAMP from ' + tableName + ' a WHERE datediff(day, ' + strDay + ", a.TIMESTAMP) = 0 and  datediff(month, " + strDay + ", a.timestamp)=0 and  datediff(year, " + strDay + ", a.timestamp)=0 and a.VALUE = 1 and a.TIMESTAMP > '" + str(lowBound) + "' and a.TIMESTAMP < '" + str(upperBound) + "' ORDER BY a.TIMESTAMP ASC"
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if not row: continue
            trueValsTemp[tableName] = row[0]
        for n in range(0, 36):
            time = datetime.datetime.combine(day, datetime.time(3,45))
            time = time + datetime.timedelta(0,300)*n
            fansOn = 0
            for tableName in trueValsTemp:
                if trueValsTemp[tableName] == None: continue
 
                if trueValsTemp[tableName] < time:
                    fansOn += 1
            if fansOn >= 5:
                val = time
                break
        if val == None:
            val = datetime.datetime.combine(day, datetime.time(6,00))
        return val.time()




class FilteredDerivativeStartupLex(FilteredDerivativeBase):
    '''
    This is the master class for the analysis, and will be the one to carry out the grid search
    over possible values of windowSize, derivSpace, and contiguousVals.  This accepts training and
    test dates, a final prediction date, the range of parameters to be searched, in tuple form, as well
    as some extra specifics-parameters
    '''



    def __init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate = None, windowSize = (1, 7), derivSpace = (2,8), contiguousVals = (1,4), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = False, FDtimeTuple = (datetime.time(3,45), datetime.time(7,15))):
        FilteredDerivativeBase.__init__(self, conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, finalPredictionDate , windowSize , derivSpace , contiguousVals , valueTable , includeWeekends , lookForNegs, FDtimeTuple)




    def populateWithDates(self, start_date, end_date, setValueTable = True):
        predictionTable = 'Space_Temperature_Prediction'
        for n in range(int((end_date - start_date).days) + 1):
            day = start_date + datetime.timedelta(n)
            strDay = day.strftime("'%Y-%m-%d'")
            if day.weekday() == 6 or day.weekday() == 5:
                if self.includeWeekends == False:
                    continue
            self.predictionDataTable[day] = {}
            for floor in self.floorList:
                query = 'Select a.Prediction_DateTime, a.Prediction_Value \
                FROM ' + predictionTable + " a \
                INNER JOIN (SELECT MAX(c.RUN_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime  \
                FROM " +  predictionTable +  " c \
                WHERE datediff(day, " + strDay + ", c.Prediction_DateTime)=0 and datediff(month, " + strDay + ", c.Prediction_DateTime)=0 and datediff(year, " + strDay + ", c.Prediction_DateTime)=0\
                GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime \
                WHERE datediff(day, " + strDay + ", a.Prediction_DateTime)=0 and datediff(month, " + strDay + ", a.Prediction_DateTime)=0 and datediff(year, " + strDay + ", a.Prediction_DateTime)=0 and a.Quadrant = '" + floor  + "' and a.Run_DateTime=b.RunDateTime \
                Order By a.prediction_DateTime"

                self.cursor.execute(query) 
                Predictions = []
                rows = self.cursor.fetchall()
                for i in range(len(rows)):
                    Predictions.append((rows[i][0], rows[i][1]))
                self.predictionDataTable[day][floor] = Predictions

            if setValueTable == True:
                self.trueValTableKeyDate[day] = self.valQueryFunction(day)

                
    def valQueryFunction(self,day):
        '''
        In this funciton, we assume that the valueTable parameter is actually a list of column name values for the table ExtendedLogCombinedAll

        '''
        strDay = day.strftime("'%Y-%m-%d'")
        lowBound = datetime.datetime.combine(day, datetime.time(03,45))
        upperBound = datetime.datetime.combine(day, datetime.time(8,15))
        trueValsTemp = {}
        fansOn = 0
        val = None
        for tup in self.valueTable:
            trueValsTemp[tup] = None
            query = 'Select a.DateTimeEDT, a.PointValue \
            FROM ExtendedLogCombinedAll a \
            WHERE datediff(day, ' + strDay + ", a.DateTimeEDT) = 0 and datediff(month, " + strDay + ", a.DateTimeEDT) = 0 and datediff(year, " + strDay + ", a.DateTimeEDT) = 0 \
            and a.PointValue > 0  and a.DateTimeEDT > '" + str(lowBound) + "' and a.DateTimeEDT < '" + str(upperBound) + "' \
            and a.Controller = '" + tup[0] + "' and a.SubController = '" + tup[1] + "' and a.PointName = '" + tup[2] + "'\
            ORDER BY a.DateTimeEDT ASC"
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if not row: continue
            #we now have the value; however, we have to convert decimal values of "Point Value" to the corresponding correct times:
            recTime = row[0]
            recVal = row[1]
            recTimeHours = recTime.hour
            if recVal < 1:
                realTimeHours = recTimeHours - 1
                realTimeMin = int(60*recVal)
            else:
                realTimeHours = recTimeHours
                realTimeMin = 0
            realTime = datetime.datetime.combine(day, datetime.time(realTimeHours, realTimeMin))
            trueValsTemp[tup] = realTime
        for n in range(0, 65):
            time = datetime.datetime.combine(day, datetime.time(3,45))
            time = time + datetime.timedelta(0,300)*n
            fansOn = 0
            for tup in trueValsTemp:
                if trueValsTemp[tup] == None: continue
 
                if trueValsTemp[tup] < time:
                    fansOn += 1
            if fansOn >= 5:
                val = time
                break
        if val == None:
            val = datetime.datetime.combine(day, datetime.time(8,00))
        return val.time()
    
    
class DayOfFilteredDeriv():
    '''
    This class's constructor accepts values for a day, and a
    floorList and calculates all filtered derivative values for the day;
    it will also find the 
    '''
    
    def __init__(self, predictionDataTable, trueValTableKeyDate, date, floorList, windowSize = 11, derivSpace= 6, contiguousVals = 5, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        '''

        '''
        self.windowSize = windowSize
        self.derivSpace = derivSpace
        self.contiguousVals= contiguousVals
        self.PredictionsKeyFloor = {}
        self.filteredDerivativeKeyFloor = {}
        self.calcdTimeValuesKeyFloor = {}
        self.trueTime = None
        self.date = date
        self.floorList = floorList
        self.lookForNegs = lookForNegs
        self.FDtimeTuple = FDtimeTuple
        for floor in floorList: 
            self.PredictionsKeyFloor[floor] = predictionDataTable[date][floor]
            if date in trueValTableKeyDate:
                self.trueTime = trueValTableKeyDate[date]
            self.filteredDerivativeKeyFloor[floor] = self.calcFilteredDerivative(self.PredictionsKeyFloor[floor], windowSize, derivSpace)
            self.calcdTimeValuesKeyFloor[floor] = self.ReccomendationGenerator(self.filteredDerivativeKeyFloor[floor], contiguousVals)


    def calcFilteredDerivative(self, Predictions, windowSize, derivSpace = 6):
        k = int(windowSize/2) - 1 * (windowSize%2 == 0)
        filtered = []
        for i in range(len(Predictions) - windowSize + 1):
            average = 0
            for j in range(i, i+windowSize):
                average = average + Predictions[j][1]
            average = average/windowSize
            filtered.append((Predictions[i+k][0], average))
        filteredDeriv = []
        count = 0
        for i in range(derivSpace, len(filtered)):
                filteredDeriv.append((filtered[i][0], filtered[i][1] - filtered[i-derivSpace][1]))
                if self.lookForNegs != True:
                    filteredDeriv[count] =  (filteredDeriv[count][0], -1* filteredDeriv[count][1])
                count += 1
        return filteredDeriv

    def plot(self, filteredDerivative = True, predictionData = False, withTrueTime = False, estimatedTime = None):
        '''
        function to plot the filtered derivative, the true rampdown value (if it exists), and/or the estimated rampdown time
        '''
        colors = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow', 'white', 'black', 'brown', 'Aqua', 'DarkGray', 'DarkKhaki', 'DarkMagenta', 'Indigo', 'LightCoral', 'LawnGreen', 'Fuchsia', 'FireBrick', 'deepskyblue', 'Navy', 'OrangeRed', 'PaleVioletRed', 'Orange', 'YellowGreen']
        count = 0
        for floor in self.floorList:
            if filteredDerivative == True:
                plt.plot([times[0] for times in self.filteredDerivativeKeyFloor[floor]], [values[1] for values in self.filteredDerivativeKeyFloor[floor]], color = colors[count%len(colors)])
            plt.hold(True)
            if predictionData == True:
                plt.plot([times[0] for times in self.PredictionsKeyFloor[floor]], [values[1] for values in self.PredictionsKeyFloor[floor]], color = colors[count%len(colors)], marker = 'v')
            if withTrueTime == True:
                if self.trueTime != None:
                    plt.plot(datetime.datetime.combine(self.date, self.trueTime), 0, color = colors[count%len(colors)], marker = 'o')
            if estimatedTime != None:
                plt.plot(estimatedTime, 0, color = colors[count%len(colors)], marker = 'x')
            count += 1
        plt.xlabel('Time')
        plt.ylabel('d/dt of Temp')
        plt.show()

        
    def getXVector(self):
        X = numpy.zeros((1,len(self.floorList)))
        for i in range(len(self.floorList)):
            recTime = self.calcdTimeValuesKeyFloor[self.floorList[i]]
            if recTime == None:
                X[0,i] = 0
                continue
            numberOfMinutes = 60 * recTime.hour + recTime.minute
            X[0,i] = numberOfMinutes
        return X

    def getYVector(self):
        Y = numpy.zeros(1)
        actTime = self.trueTime
        numberOfMinutes = 60 * actTime.hour + actTime.minute
        Y[0] = numberOfMinutes
        return Y

                 

    def ReccomendationGenerator(self, filteredDeriv, contiguousVals):
        '''
        logic here is to look for contiguousVals number of contiguous negatives(positive) derivative values between the values determined by the timeTuple
        '''
        reccomendedTime = None
        negCounter = 0
        trialTime = None
        for time_value in filteredDeriv:
            if time_value[0].time() < self.FDtimeTuple[0] or time_value[0].time() > self.FDtimeTuple[1]:
                if negCounter == 0:
                    continue
            if time_value[1] < 0:
                if negCounter == 0:
                    trialTime = time_value[0]
                negCounter = negCounter + 1
            else:
                negCounter = 0
            if negCounter == contiguousVals:
                reccomendedTime = trialTime
        return reccomendedTime

    

class FilteredDerivativeTester():
    '''
    This class will hold multiple days of filtered derivatives
    to be used for testing purposes to test both the parameters
    of the filter+derivative, as well as the lasso regression itself
    '''
    def __init__(self, predictionDataTable, trueValTableKeyDate, start_date, end_date, floorList, windowSize = 11, derivSpace= 6, contiguousVals = 5, includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        self.predictionDataTable = predictionDataTable
        self.trueValTableKeyDate = trueValTableKeyDate
        self.lookForNegs = lookForNegs
        self.filteredDerivsKeyDay = {}
        self.start_date = start_date
        self.end_date = end_date
        self.windowSize = windowSize
        self.derivSpace = derivSpace
        self.contiguousVals = contiguousVals
        self.floorList = floorList
        self.numberOfDays = 0
        self.YActual = None
        self.YPredicted = None
        self.squaredError = 0
        self.FDtimeTuple = FDtimeTuple
        for n in range(int((end_date - start_date).days) +1):
            day = start_date + datetime.timedelta(n)
            if day.weekday() == 6 or day.weekday() == 5:
                if includeWeekends == False:
                    continue
            self.numberOfDays +=1
            self.filteredDerivsKeyDay[day] = DayOfFilteredDeriv(predictionDataTable, trueValTableKeyDate, day, floorList, windowSize, derivSpace, contiguousVals, lookForNegs, self.FDtimeTuple)

    def calculatePredictions(self, regressionObject):
        self.YActual = numpy.zeros((self.numberOfDays, 1))
        self.YPredicted = numpy.zeros((self.numberOfDays, 1))
        count = 0
        for day in self.filteredDerivsKeyDay:
            self.YActual[count] = self.filteredDerivsKeyDay[day].getYVector()
            pred = regressionObject.predict(self.filteredDerivsKeyDay[day].getXVector())
            self.YPredicted[count] = pred
            count += 1
        for i in range(len(self.YActual)):
            self.squaredError += (self.YActual[i] - self.YPredicted[i])**2

    def predict(self, regressionObject, predictionDate, plot = False):
        if predictionDate not in self.filteredDerivsKeyDay:
            self.filteredDerivsKeyDay[predictionDate] = DayOfFilteredDeriv(self.predictionDataTable, self.trueValTableKeyDate, predictionDate, self.floorList, self.windowSize, self.derivSpace, self.contiguousVals, self.lookForNegs, self.FDtimeTuple)
        pred = regressionObject.predict(self.filteredDerivsKeyDay[predictionDate].getXVector())
        minutes = pred%60
        hours = (pred - minutes) / 60
        predTime = datetime.time(hours, minutes)
        predDateTime = datetime.datetime.combine(predictionDate, predTime)
        if plot == True:
            self.filteredDerivsKeyDay[predictionDate].plot(True, False, False, predDateTime)
        return predDateTime

    

class FilteredDerivativeTrainer():
    '''
    This class will hold multiple days of filtered derivatives
    to be used for training/lambda selection for lasso regression
    '''
    def __init__(self, predictionDataTable, trueValTableKeyDate, start_date, end_date, floorList, windowSize = 11, derivSpace= 6, contiguousVals = 5, includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00))):
        self.filteredDerivsKeyDay = {}
        self.regressionObject = None
        self.lookForNegs = lookForNegs
        self.regressionWeightsKeyFloor = {}
        self.start_date = start_date
        self.end_date = end_date
        self.windowSize = windowSize
        self.derivSpace = derivSpace
        self.contiguousVals = contiguousVals
        self.floorList = floorList
        self.numberOfDays = 0
        self.X = None
        self.Y = None
        self.FDtimeTuple = FDtimeTuple
        for n in range(int((end_date - start_date).days)+1):
            day = start_date + datetime.timedelta(n)

            if day.weekday() == 6 or day.weekday() == 5:
                if includeWeekends == False:
                    continue
            self.numberOfDays +=1
            self.filteredDerivsKeyDay[day] = DayOfFilteredDeriv(predictionDataTable, trueValTableKeyDate, day, floorList, windowSize, derivSpace, contiguousVals, lookForNegs, self.FDtimeTuple)

    def fillRegressionWeights(self):
        self.X = numpy.zeros((self.numberOfDays, len(self.floorList)))
        self.Y = numpy.zeros((self.numberOfDays, 1))
        count = 0
        for day in self.filteredDerivsKeyDay:
            xRow = self.filteredDerivsKeyDay[day].getXVector()
            yRow = self.filteredDerivsKeyDay[day].getYVector()
            self.X[count, ::1] = xRow
            self.Y[count] = yRow
            count += 1
        self.regressionObject = LassoCV(cv = 5, verbose = False, fit_intercept = False)
        self.regressionObject.fit(self.X,self.Y)
        '''
        print(self.X)
        print(self.Y)
        print(self.regressionObject.coef_)
        print(self.regressionObject.intercept_)
        print(self.regressionObject.alphas_)
        print(self.regressionObject.alpha_)
        '''
        for i in range(len(self.floorList)):
            self.regressionWeightsKeyFloor[self.floorList[i]] = self.regressionObject.coef_[i]

    def printRegressionStats(self):
        for floor in self.regressionWeightsKeyFloor:
            print floor, self.regressionWeightsKeyFloor[floor]
        print "alpha:", self.regressionObject.alpha_


    def predict(self, predictionDate, plot = False):
        if predictionDate not in self.filteredDerivsKeyDay:
            self.filteredDerivsKeyDay[predictionDate] = DayOfFilteredDeriv(self.predictionDataTable, self.trueValTableKeyDate, predictionDate, self.floorList, self.windowSize, self.derivSpace, self.contiguousVals, self.lookForNegs, self.FDtimeTuple)
        pred = self.regressionObject.predict(self.filteredDerivsKeyDay[predictionDate].getXVector())
        minutes = pred%60
        hours = (pred - minutes) / 60
        predTime = datetime.time(hours, minutes)
        predDateTime = datetime.datetime.combine(predictionDate, predTime)
        if plot == True:
            self.filteredDerivsKeyDay[predictionDate].plot(True, False, False, predDateTime)
        return predDateTime


            
    
            
    
            
