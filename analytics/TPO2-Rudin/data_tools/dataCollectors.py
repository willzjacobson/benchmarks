
import datetime
import pyodbc

class dataCollectorBase():
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends):
        self.conn = conn
        self.cursor = cursor
        self.tableName = tableName
        self.numberOfDays = numberOfDays
        self.startDatetime = startDatetime
        self.rawDataKeyDayKeyFloor = {}
        self.includeWeekends = includeWeekends

    def getData(self):
        pass


'''
Weather database query using format as on Anderson
'''

class dataCollectorWeather(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, colName = 'TempA'):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.colName = colName

    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        self.rawDataKeyDay = {}
        print "data not specific to floor"
        predictions = []
        query = "Select a.Fcst_date, a.Date, a." + self.colName + " from " + self.tableName + " a"
        query += " WHERE a.Date > " + strBegTime
        query += " and a.Date < " + strEndTime + " ORDER BY a.Fcst_date DESC"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except:
            print "database read failed, check table name \
                        and ensure correct parameterization of db query: " + self.tableName
            return
        uniqueTSDict = {}
        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.0%f'
        for i in range(len(rows)):
            rows[i][1] = datetime.datetime.strptime(rows[i][1], DATETIME_FORMAT)
            if rows[i][1].replace(second = 0, microsecond =0) not in uniqueTSDict:
                predictions.append((rows[i][1].replace(second = 0, microsecond =0), rows[i][2]))
                uniqueTSDict[rows[i][1].replace(second = 0, microsecond =0)] = 1
        for ts, val in predictions:
            if ts.date() not in self.rawDataKeyDay:
                if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                    if self.includeWeekends == False:
                        continue
                self.rawDataKeyDay[ts.date()] = []
                print "Query on table name " + str(self.tableName) + " completed for date: " + str(ts.date())
            if ts.date() == self.startDatetime.date():
                self.maxTS = ts.replace(second = 0, microsecond =0)
            self.rawDataKeyDay[ts.date()].append((ts, val))

'''
Building Agnostic Data Collectors that follow the regularized format of Rudin's normalized point list
'''

class dataCollectorBMSInput(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, equalityConstraintList = ['*'], constraintValListKeyFloor = ['*']):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.equalityConstraintList = equalityConstraintList
        self.constraintValListKeyFloor = constraintValListKeyFloor

    def getData(self):
        if self.equalityConstraintList[0] == '*':
            self.getDataNoFloor()
        else:
            self.getDataFloorData()

    def getDataNoFloor(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        
        self.rawDataKeyDayKeyFloor = None
        self.rawDataKeyDay = {}
        print "data not specific to floor"
        predictions = []
        query = "Select a.TIMESTAMP, a.Value from" + self.tableName + " a"
        query += " WHERE a.TIMESTAMP > " + strBegTime
        query += " and a.TIMESTAMP < " + strEndTime + " ORDER BY a.TIMESTAMP ASC"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except:
            print "database read failed, check table name \
                        and ensure correct parameterization of db query: " + self.tableName
            return
        for i in range(len(rows)):
            predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
        for ts, val in predictions:
            if ts.date() not in self.rawDataKeyDay:
                if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                    if self.includeWeekends == False:
                        continue
                self.rawDataKeyDay[ts.date()] = []
                print "Query on table name " + str(self.tableName) + " completed for date: " + str(ts.date())
            if ts.date() == self.startDatetime.date():
                self.maxTS = ts.replace(second = 0, microsecond =0)
            self.rawDataKeyDay[ts.date()].append((ts, val))

    def getDataFloorData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        for floor in self.constraintValListKeyFloor:
            if len(self.equalityConstraintList) != len(self.constraintValListKeyFloor[floor]):
                print "equality constraints do not match with values for floor " + str(floor)
                print self.equalityConstraintList
                print self.constraintValListKeyFloor[floor]
                continue
            predictions = []
            constraintQueryList = [" a." + str(self.equalityConstraintList[i]) +
                                    " = " + str(self.constraintValListKeyFloor[floor][i]) +
                                    " and" for i in range(len(self.constraintValListKeyFloor[floor]))] 
            query = "Select a.TIMESTAMP, a.Value from " + self.tableName + " a"
            query += " WHERE a.TIMESTAMP > " + strBegTime+ " and"
            for consQuery in constraintQueryList: 
                query += consQuery
            query += " a.TIMESTAMP < "+  strEndTime
            query += " ORDER BY a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()

            except:
                print query
                print "database read failed, check table name \
                            and ensure correct parameterization of db query: " + self.tableName
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print "Query on table name " + str(self.tableName) + " completed for date: " + str(ts.date())
                if floor not in self.rawDataKeyDayKeyFloor[ts.date()]:
                        self.rawDataKeyDayKeyFloor[ts.date()][floor] = []
                if ts.date() == self.startDatetime.date():
                        self.maxTS = ts.replace(second = 0, microsecond =0)
                self.rawDataKeyDayKeyFloor[ts.date()][floor].append((ts, val))


class dataCollectorBMSInputParkStartup(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, equalityConstraintList = ['FLOOR'], constraintValList = ['*']):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.equalityConstraintList = equalityConstraintList
        self.constraintValList = constraintValList
        self.tableName = tableName
        self.rawDataKeyDay = {}

    def getData(self):
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day + datetime.timedelta(-n)
            lowBound = datetime.datetime.combine(day, datetime.time(03,45))
            upperBound = datetime.datetime.combine(day, datetime.time(8,00))
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            strDay = day.strftime("'%Y-%m-%d'")
            predictions = []
            trueValsTemp = {}
            for iterable in self.constraintValList:
                trueValsTemp[iterable] = None
                query = 'Select a.TIMESTAMP from ' + self.tableName + ' a WHERE datediff(day, ' + strDay
                query+= ", a.TIMESTAMP) = 0 and  datediff(month, " + strDay
                query+= ", a.timestamp)=0 and  datediff(year, " + strDay 
                query+= ", a.timestamp)=0 and a.VALUE = 1 and a.TIMESTAMP > '" + str(lowBound)
                query+= "' and a.TIMESTAMP < '" + str(upperBound) + "'"
                query += " and a." + str(self.equalityConstraintList[0]) + " = " + str(iterable)
                query += " ORDER BY a.TIMESTAMP ASC"
                try:
                    #print query
                    self.cursor.execute(query)
                    row = self.cursor.fetchone()
                except:
                    print "database read failed in Park Startup, check table name: " + self.tableName
                    return
                if not row:
                    print "value not recovered for table name: " + self.tableName+ "for date " + str(day)
                    continue
                trueValsTemp[iterable] = row[0]
            val = None
            for k in range(0, 48):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for iterable in trueValsTemp:
                    if trueValsTemp[iterable] == None: continue
     
                    if trueValsTemp[iterable] < time:
                        fansOn += 1
                if fansOn >= 5:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(6,33))
            print "Park Startup collected for day" + str(day) +" as " + str(val)
            self.rawDataKeyDay[day] = val

class dataCollectorBMSInput40E52Startup(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, equalityConstraintList = ['FLOOR'], constraintValList = ['*']):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.equalityConstraintList = equalityConstraintList
        self.constraintValList = constraintValList
        self.tableName = tableName
        self.rawDataKeyDay = {}

    def getData(self):
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day + datetime.timedelta(-n)
            lowBound = datetime.datetime.combine(day, datetime.time(03,45))
            upperBound = datetime.datetime.combine(day, datetime.time(8,00))
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            strDay = day.strftime("'%Y-%m-%d'")
            predictions = []
            trueValsTemp = {}
            for iterable in self.constraintValList:
                trueValsTemp[iterable] = None
                query = 'Select a.TIMESTAMP from ' + self.tableName + ' a WHERE datediff(day, ' + strDay
                query+= ", a.TIMESTAMP) = 0 and  datediff(month, " + strDay
                query+= ", a.timestamp)=0 and  datediff(year, " + strDay 
                query+= ", a.timestamp)=0 and a.VALUE = 1 and a.TIMESTAMP > '" + str(lowBound)
                query+= "' and a.TIMESTAMP < '" + str(upperBound) + "'"
                query += " and a." + str(self.equalityConstraintList[0]) + " = " + str(iterable)
                query += " ORDER BY a.TIMESTAMP ASC"
                try:
                    #print query
                    self.cursor.execute(query)
                    row = self.cursor.fetchone()
                except:
                    print "database read failed in 40E5 Startup, check table name: " + self.tableName
                    return
                if not row:
                    print "value not recovered for table name: " + self.tableName+ "for date " + str(day) + " for iterable: " + str(iterable)
                    continue
                trueValsTemp[iterable] = row[0]
            val = None
            for k in range(0, 48):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for iterable in trueValsTemp:
                    if trueValsTemp[iterable] == None: continue
     
                    if trueValsTemp[iterable] < time:
                        fansOn += 1
                if fansOn >= 3:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(6,33))
            print "40E5 Startup collected for day" + str(day) +" as " + str(val)
            self.rawDataKeyDay[day] = val

class dataCollectorBMSInput1BPStartup(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, equalityConstraintList = ['FLOOR'], constraintValList = ['*']):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.equalityConstraintList = equalityConstraintList
        self.constraintValList = constraintValList
        self.tableName = tableName
        self.rawDataKeyDay = {}

    def getData(self):
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day + datetime.timedelta(-n)
            lowBound = datetime.datetime.combine(day, datetime.time(03,45))
            upperBound = datetime.datetime.combine(day, datetime.time(8,00))
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            strDay = day.strftime("'%Y-%m-%d'")
            predictions = []
            trueValsTemp = {}
            for iterable in self.constraintValList:
                trueValsTemp[iterable] = None
                query = 'Select a.TIMESTAMP from ' + self.tableName + ' a WHERE datediff(day, ' + strDay
                query+= ", a.TIMESTAMP) = 0 and  datediff(month, " + strDay
                query+= ", a.timestamp)=0 and  datediff(year, " + strDay 
                query+= ", a.timestamp)=0 and a.VALUE = 1 and a.TIMESTAMP > '" + str(lowBound)
                query+= "' and a.TIMESTAMP < '" + str(upperBound) + "'"
                query += " and a." + str(self.equalityConstraintList[0]) + " = " + str(iterable)
                query += " ORDER BY a.TIMESTAMP ASC"
                try:
                    #print query
                    self.cursor.execute(query)
                    row = self.cursor.fetchone()
                except:
                    print "database read failed in 1BP Startup, check table name: " + self.tableName
                    return
                if not row:
                    print "value not recovered for table name: " + self.tableName+ "for date " + str(day)
                    continue
                trueValsTemp[iterable] = row[0]
            val = None
            for k in range(0, 48):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for iterable in trueValsTemp:
                    if trueValsTemp[iterable] == None: continue
     
                    if trueValsTemp[iterable] < time:
                        fansOn += 1
                if fansOn >= 3:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(6,33))
            print "1BP Startup collected for day" + str(day) +" as " + str(val)
            self.rawDataKeyDay[day] = val

        
            

class dataCollectorBMSInputLexStartup(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                            includeWeekends, equalityConstraintList = ['FLOOR'], constraintValListKeyFloor = ['*']):
        dataCollectorBase.__init__(self,conn,cursor,tableName, numberOfDays,startDatetime,includeWeekends)
        self.equalityConstraintList = equalityConstraintList
        self.constraintValListKeyFloor = constraintValListKeyFloor
        self.rawDataKeyDay = {}



    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        for floor in self.constraintValListKeyFloor:
            if len(self.equalityConstraintList) != len(self.constraintValListKeyFloor[floor]):
                print "equality constraints do not match with values for floor " + str(floor)
                continue
            predictions = []
            constraintQueryList = [" a." + str(self.equalityConstraintList[i]) +
                                    " = " + str(self.constraintValListKeyFloor[floor][i]) +
                                    " and" for i in range(len(self.constraintValListKeyFloor[floor]))] 
            query = "Select a.TIMESTAMP, a.Value from " + self.tableName + " a"
            query += " WHERE a.TIMESTAMP > " + strBegTime + " and"
            for consQuery in constraintQueryList: 
                query += consQuery
            query += " a.Value > 0 and"
            query += " a.TIMESTAMP < "+  strEndTime
            query += " ORDER BY a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
            except:
                print query
                print "database read failed, check table name \
                            and ensure correct parameterization of db query: " + self.tableName
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print "Data from " + str(self.tableName) + " gathered for date: " + str(ts.date())
                if floor not in self.rawDataKeyDayKeyFloor[ts.date()]:
                        self.rawDataKeyDayKeyFloor[ts.date()][floor] = []
                if ts.date() == self.startDatetime.date():
                        self.maxTS = ts.replace(second = 0, microsecond =0)
                self.rawDataKeyDayKeyFloor[ts.date()][floor].append((ts, val))
                
        for day in self.rawDataKeyDayKeyFloor:
            trueValsTemp = {}
            for floor in self.rawDataKeyDayKeyFloor[day]:
                recTime = self.rawDataKeyDayKeyFloor[day][floor][0][0] #get the time of the first nonzero fan value for the given floor
                recVal = self.rawDataKeyDayKeyFloor[day][floor][0][1] #get the value of the first nonzero fan value for the given floor
                recTimeHours = recTime.hour
                recTimeMin = recTime.minute
                if recVal < 1:
                    if recTimeMin == 0:
                        realTimeHours = recTimeHours - 1
                        realTimeMin = int(45 + recVal*15)
                    else:
                        realTimeHours = recTimeHours
                        realTimeMin = int(recTimeMin - 15 + recVal*15)
                else:
                    realTimeHours = recTimeHours
                    realTimeMin = recTimeMin
                realTime = datetime.datetime.combine(day, datetime.time(realTimeHours, realTimeMin))
                trueValsTemp[floor] = realTime
            val = None
            for k in range(0, 80):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for floor in trueValsTemp:
                    if trueValsTemp[floor] == None: continue
     
                    if trueValsTemp[floor] < time:
                        fansOn += 1
                if fansOn >= 3:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(7,30))
                self.rawDataKeyDay[day] = val
                print "fan threshhold not reached, default time used"
            else:
                self.rawDataKeyDay[day] = val + datetime.timedelta(minutes=-20)
            print "startup time recorded for day " + str(day) + " as " + str(self.rawDataKeyDay[day])
        for n in range(self.numberOfDays + 1):
            day = begTime.date() + datetime.timedelta(n)
            if day not in self.rawDataKeyDay:
                val = datetime.datetime.combine(day, datetime.time(7,30))
                print "default startup time recorded for day " + str(day) + " as " + str(val)
                self.rawDataKeyDay[day] = val
        
# dummy data collector for 40E52 rampdown

class dataCollector40E52Rampdown(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,includeWeekends=False):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.rawDataKeyDay = {}
        
    def getData(self):
        strTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            strDay = day.strftime("'%Y-%m-%d'")
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            query ='Select a.TIMESTAMP from ' + self.tableName
            query+= ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0'
            query+= " Order by a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                val= self.cursor.fetchone()
                if val == None:
                    val = datetime.datetime.combine(day, datetime.time(16,00))
                    print "David needs to update the rampdown tables..."
                else:
                    val = val[0]
            except:
                print "database read failed in park rampdown, check table name: " + str(self.tableName)
                continue
            if not val:
                print "value not recovered for park rampdown for date: " + str(strDay)
                val = datetime.datetime.combine(day, datetime.time(16,00))
            self.rawDataKeyDay[day] = val

# dummy data collector for 1BP

class dataCollector1BPRampdown(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,includeWeekends=False):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.rawDataKeyDay = {}
        
    def getData(self):
        strTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            strDay = day.strftime("'%Y-%m-%d'")
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            query ='Select a.TIMESTAMP from ' + self.tableName
            query+= ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0'
            query+= " Order by a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                val= self.cursor.fetchone()
                if val == None:
                    val = datetime.datetime.combine(day, datetime.time(16,00))
                    print "David needs to update the rampdown tables..."
                else:
                    val = val[0]
            except:
                print "database read failed in park rampdown, check table name: " + str(self.tableName)
                continue
            if not val:
                print "value not recovered for park rampdown for date: " + str(strDay)
                val = datetime.datetime.combine(day, datetime.time(16,00))
            self.rawDataKeyDay[day] = val
'''
Building Agnostic Data Collectors (Following Ashish's table standard)
'''

class dataCollectorSpaceTempPredictions(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime, floorList,
                 tableFloorDesignator, includeWeekends=True, quadrantDict = None):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.floorList = floorList
        self.tableFloorDesignator = tableFloorDesignator
        self.maxTS = None
        self.quadrantDict = quadrantDict
        #print quadrantDict
        
    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        self.rawDataKeyFloorKeyDay = {}
        for floor in self.floorList:
            predictions = []
            query = "Select a.Prediction_DateTime, a.Prediction_Value from " + self.tableName + " a"
            query += " INNER JOIN (SELECT MAX(c.Run_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime"
            query += " FROM "+ self.tableName +" c WHERE c.prediction_DateTime > " + strBegTime
            query += " GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime"
            query += " WHERE a.Prediction_DateTime > " + strBegTime + " and a." + self.tableFloorDesignator + " = " + str(floor)
            # next two lines are never used as of now...
            if self.quadrantDict!= None:
                #print "quadrant Dict is not None"
                query += " and a.Quadrant = " + str(self.quadrantDict[floor][0])
            query += " and a.Run_DateTime=b.RunDateTime and a.Prediction_DateTime < " + strEndTime +" ORDER BY a.Prediction_DateTime ASC"

            lastDate = None
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                #print query
            except:
                print "database read failed in spt predictions, check table name: " + self.tableName
                print query
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if lastDate == None:
                    lastDate = ts.date()
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print "Space Temp Predictions Queried and Recieved for date: " + str(ts.date())
                if floor not in self.rawDataKeyDayKeyFloor[ts.date()]:
                    self.rawDataKeyDayKeyFloor[ts.date()][floor] = []
                    #print "added floor " + str(floor)
                if ts.date() == self.startDatetime.date():
                    self.maxTS = ts.replace(second = 0, microsecond =0)
                    #print "size of space temp pred for date, floor " +str(ts.date()) + ", " + str(floor) + ": " + str(len(self.rawDataKeyDayKeyFloor[ts.date()][floor]))
                #print((ts, val))
                self.rawDataKeyDayKeyFloor[ts.date()][floor].append((ts, val))
                #if ts.date() != lastDate:
                    #print "size of space temp pred for date, floor " +str(lastDate) + ", " + str(floor) + ": " + str(len(self.rawDataKeyDayKeyFloor[lastDate][floor]))
                lastDate = ts.date()



class dataCollectorSteamPredictions(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                 includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays,
                                   startDatetime, includeWeekends)
        self.maxTS = None
        self.rawDataKeyDay = {}
        
    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        predictions = []
        query = "Select a.Prediction_DateTime, a.Prediction_Value from " + self.tableName + " a"
        query += " INNER JOIN (SELECT MAX(c.Run_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime"
        query += " FROM "+ self.tableName +" c WHERE c.Prediction_DateTime > " + strBegTime
        query += " GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime"
        query += " WHERE a.Prediction_DateTime > " + strBegTime
        query += " and a.Run_DateTime=b.RunDateTime and a.Prediction_DateTime < " + strEndTime +" ORDER BY a.Prediction_DateTime ASC"

                
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except:
            print "database read failed in steam predictions, check table name: " + self.tableName
            return
        for i in range(len(rows)):
            predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
        for ts, val in predictions:
            if ts.date() not in self.rawDataKeyDay:
                if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                    if self.includeWeekends == False:
                        continue
                self.rawDataKeyDay[ts.date()] = []
                print "Steam Predictions Queried and Recieved for date: " + str(ts.date())
            if ts.date() == self.startDatetime.date():
                self.maxTS = ts.replace(second = 0, microsecond =0)
            self.rawDataKeyDay[ts.date()].append((ts, val))

class dataCollectorOccupancyPredictions(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                 includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays,
                                   startDatetime, includeWeekends)
        self.maxTS = None
        self.rawDataKeyDay = {}
        
    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        predictions = []
        query = "Select a.Prediction_DateTime, a.Prediction_Value from " + self.tableName + " a"
        query += " INNER JOIN (SELECT MAX(c.Run_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime"
        query += " FROM "+ self.tableName +" c WHERE c.Prediction_DateTime > " + strBegTime
        query += " GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime"
        query += " WHERE a.Prediction_DateTime > " + strBegTime
        query += " and a.Run_DateTime=b.RunDateTime and a.Prediction_DateTime < " + strEndTime +" ORDER BY a.Prediction_DateTime ASC"

                
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except:
            print "database read failed in occupancy predictions, check table name: " + self.tableName
            print query
            return
        for i in range(len(rows)):
            predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
        for ts, val in predictions:
            if ts.date() not in self.rawDataKeyDay:
                if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                    if self.includeWeekends == False:
                        continue
                self.rawDataKeyDay[ts.date()] = []
                print "Occupancy Predictions Queried and Recieved for date: " + str(ts.date())
            if ts.date() == self.startDatetime.date():
                self.maxTS = ts.replace(second = 0, microsecond =0)
            self.rawDataKeyDay[ts.date()].append((ts, val))


class dataCollectorElectricityPredictions(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                 includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays,
                                   startDatetime, includeWeekends)
        self.maxTS = None
        self.rawDataKeyDay = {}
        
    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        predictions = []
        query = "Select a.Prediction_DateTime, a.Prediction_Value from " + self.tableName + " a"
        query += " INNER JOIN (SELECT MAX(c.Run_DateTime) as RunDateTime, c.Prediction_DateTime as predDateTime"
        query += " FROM "+ self.tableName +" c WHERE c.Prediction_DateTime > " + strBegTime
        query += " GROUP BY c.Prediction_DateTime) b ON a.Run_DateTime = b.RunDateTime and a.Prediction_DateTime = b.predDateTime"
        query += " WHERE a.Prediction_DateTime > " + strBegTime
        query += " and a.Run_DateTime=b.RunDateTime and a.Prediction_DateTime < " + strEndTime +" ORDER BY a.Prediction_DateTime ASC"

                
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except:
            print "database read failed in electricity predictions, check table name: " + self.tableName
            return
        for i in range(len(rows)):
            predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
        for ts, val in predictions:
            if ts.date() not in self.rawDataKeyDay:
                if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                    if self.includeWeekends == False:
                        continue
                self.rawDataKeyDay[ts.date()] = []
                print "Electricity Queried and Recieved for date: " + str(ts.date())
            if ts.date() == self.startDatetime.date():
                self.maxTS = ts.replace(second = 0, microsecond =0)
            self.rawDataKeyDay[ts.date()].append((ts, val))

##########################################################################################
# All of the following Data Collectors Work only with old local databases Bucky and Bell #
##########################################################################################


'''
560 Lex specific data collectors
todo: index the database to optimize the runtime of the LexingtonPointNameData dataCollector's query
'''

class dataCollectorLexingtonPointNameData(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime, floorList,
                 pointName, tableFloorDesignator, includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.floorList = floorList
        self.tableFloorDesignator = tableFloorDesignator
        self.pointName = pointName

    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        predictions = []
        for floor in self.floorList:
            predictions = []
            query = "Select a.DateTimeEDT, a.PointValue from " + self.tableName + " a"
            query += " WHERE a.DateTimeEDT > " + strBegTime
            query += " and a." +str(self.tableFloorDesignator) + "= " + str(floor)
            query += " and a.PointName = '" + str(self.pointName) +"'"
            query += " and a.DateTimeEDT < " + strEndTime +" ORDER BY a.DateTimeEDT ASC"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
            except:
                print "database read failed in lexington datacollector for " + str(self.pointName)
                print "query: "
                print query
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print str(self.pointName) + " Queried and Recieved for date: " + str(ts.date())
                if floor not in self.rawDataKeyDayKeyFloor[ts.date()]:
                    self.rawDataKeyDayKeyFloor[ts.date()][floor] = []
                    #print "added floor " + str(floor)
                if ts.date() == self.startDatetime.date():
                    self.maxTS = ts.replace(second = 0, microsecond =0)
                #print((ts, val))
                self.rawDataKeyDayKeyFloor[ts.date()][floor].append((ts, val))


class dataCollectorLexStartup(dataCollectorBase):
    def __init__(self,conn,cursor,tableName, numberOfDays, startDatetime, floorList, includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime,
                                   includeWeekends)
        self.floorList = floorList
        self.rawDataKeyDay = {}

    def getData(self):
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day + datetime.timedelta(-n)
            lowBound = datetime.datetime.combine(day, datetime.time(03,45))
            upperBound = datetime.datetime.combine(day, datetime.time(11,00))
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            strDay = day.strftime("'%Y-%m-%d'")
            predictions = []
            trueValsTemp = {}
            for tup in self.floorList:
                trueValsTemp[tup] = None
                query = 'Select a.DateTimeEDT, a.PointValue FROM ' + str(self.tableName) + " a"
                query += " WHERE datediff(day, " + strDay + ", a.DateTimeEDT) = 0"
                query += " and a.Controller = '" + tup[0] + "' and a.SubController = '" + tup[1] + "'"
                query += " and a.PointName = '" + tup[2] + "'"
                query += " and a.PointValue > 0  and a.DateTimeEDT > '" + str(lowBound) + "' and a.DateTimeEDT < '"
                query += str(upperBound) + "' ORDER BY a.DateTimeEDT ASC"
                try:
                    self.cursor.execute(query)
                    row = self.cursor.fetchone()
                except:
                    print "database read failed in Lex Startup, check table name: " + str(tup)
                    return
                if not row:
                    #print "value not recovered for table name: " + str(tup)
                    continue
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
            for k in range(0, 80):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for tup in trueValsTemp:
                    if trueValsTemp[tup] == None: continue
     
                    if trueValsTemp[tup] < time:
                        fansOn += 1
                if fansOn >= 5:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(6,30))
            print "startup time recorded for day " + str(day) + " as " + str(val)
            self.rawDataKeyDay[day] = val


class dataCollectorLexRampdown(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,includeWeekends=False):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.rawDataKeyDay = {}

    def getData(self):
        strTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            strDay = day.strftime("'%Y-%m-%d'")
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            query ='Select a.TIMESTAMP from ' + self.tableName
            query+= ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0'
            query+= " Order by a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                val = self.cursor.fetchone()
                if val == None:
                    val = datetime.datetime.combine(day, datetime.time(16,00))
                    print "David needs to update the rampdown tables..."
                else:
                    val = val[0]
            except:
                print "database read failed in lexington rampdown, check table name: " + str(self.tableName)
                return
            if not val:
                print "value not recovered for lexington rampdown for date: " + str(strDay)
                val = datetime.datetime.combine(day, datetime.time(16,00))
            self.rawDataKeyDay[day] = val

'''
345 Park specific data collectors
'''

class dataCollectorSpaceTemp(dataCollectorBase):
    def __init__(self, conn, cursor, tableNameList, numberOfDays, startDatetime , floorList,
                 floorsKeyTableName, includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableNameList,
                                   numberOfDays, startDatetime, includeWeekends)
        self.tableNameList = tableNameList
        self.floorsKeyTableName = floorsKeyTableName
        self.maxTS = None

    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        '''
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            rawDataKeyFloor = {}
        '''
        for tableName in self.tableNameList:
            predictions = []
            query = "Select a.TIMESTAMP, a.Value from " + tableName + " a"
            query += " WHERE a.TIMESTAMP > " + strBegTime  
            query += " and a.TIMESTAMP < " + strEndTime +" ORDER BY a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
            except:
                print "database read failed in spt, check table name: " + tableName
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print "Space Temp Queried and Recieved for date: " + str(ts.date())
                if self.floorsKeyTableName[tableName] not in self.rawDataKeyDayKeyFloor[ts.date()]:
                    self.rawDataKeyDayKeyFloor[ts.date()][self.floorsKeyTableName[tableName]] = []
                    #print "added floor " + str(floor)
                if ts.date() == self.startDatetime.date():
                    self.maxTS = ts.replace(second = 0, microsecond =0)
                #print((ts, val))
                self.rawDataKeyDayKeyFloor[ts.date()][self.floorsKeyTableName[tableName]].append((ts, val))



class dataCollectorParkStartup(dataCollectorBase):
    def __init__(self,conn,cursor,tableNameList, numberOfDays, startDatetime, includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableNameList, numberOfDays, startDatetime,
                                   includeWeekends)
        self.tableNameList = tableNameList
        self.rawDataKeyDay = {}

    def getData(self):
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day + datetime.timedelta(-n)
            lowBound = datetime.datetime.combine(day, datetime.time(03,45))
            upperBound = datetime.datetime.combine(day, datetime.time(8,00))
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            strDay = day.strftime("'%Y-%m-%d'")
            predictions = []
            trueValsTemp = {}
            for tableName in self.tableNameList:
                trueValsTemp[tableName] = None
                query = 'Select a.TIMESTAMP from ' + tableName + ' a WHERE datediff(day, ' + strDay
                query+= ", a.TIMESTAMP) = 0 and  datediff(month, " + strDay
                query+= ", a.timestamp)=0 and  datediff(year, " + strDay 
                query+= ", a.timestamp)=0 and a.VALUE = 1 and a.TIMESTAMP > '" + str(lowBound)
                query+= "' and a.TIMESTAMP < '" + str(upperBound) + "' ORDER BY a.TIMESTAMP ASC"
                try:
                    self.cursor.execute(query)
                    row = self.cursor.fetchone()
                except:
                    print "database read failed in Park Startup, check table name: " + tableName
                    return
                if not row:
                    print "value not recovered for table name: " + tableName
                    continue
                trueValsTemp[tableName] = row[0]
            for k in range(0, 48):
                time = datetime.datetime.combine(day, datetime.time(3,45))
                time = time + datetime.timedelta(0,300)*k
                fansOn = 0
                for tableName in trueValsTemp:
                    if trueValsTemp[tableName] == None: continue
 
                    if trueValsTemp[tableName] < time:
                        fansOn += 1
                if fansOn >= 5:
                    val = time
                    break
            if val == None:
                val = datetime.datetime.combine(day, datetime.time(6,30))
            print "Park Startup collected for day" + str(day)
            self.rawDataKeyDay[day] = val

class dataCollectorParkRampdown(dataCollectorBase):
    def __init__(self, conn, cursor, tableName, numberOfDays, startDatetime,includeWeekends=False):
        dataCollectorBase.__init__(self, conn, cursor, tableName, numberOfDays, startDatetime, includeWeekends)
        self.rawDataKeyDay = {}
        
    def getData(self):
        strTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            strDay = day.strftime("'%Y-%m-%d'")
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            query ='Select a.TIMESTAMP from ' + self.tableName
            query+= ' a WHERE datediff(day, ' + strDay + ', a.TIMESTAMP) = 0'
            query+= " Order by a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                val= self.cursor.fetchone()
                if val == None:
                    val = datetime.datetime.combine(day, datetime.time(16,00))
                    print "David needs to update the rampdown tables..."
                else:
                    val = val[0]
            except:
                print "database read failed in park rampdown, check table name: " + str(self.tableName)
                continue
            if not val:
                print "value not recovered for park rampdown for date: " + str(strDay)
                val = datetime.datetime.combine(day, datetime.time(16,00))
            self.rawDataKeyDay[day] = val
        



class dataCollectorSupplyAir(dataCollectorBase):
    def __init__(self,conn,cursor,tableNameList, numberOfDays, startDatetime,
                 floorList, floorsKeyTableName, includeWeekends=True):
        dataCollectorBase.__init__(self, conn, cursor, tableNameList, numberOfDays,
                                   startDatetime, includeWeekends)
        self.floorList = floorList
        self.floorsKeyTableName = floorsKeyTableName
        self.tableNameList = tableNameList  
        self.maxTS = None

    def getData(self):
        strEndTime = self.startDatetime.strftime("'%Y-%m-%d %H:%M:%S'")
        begTime = datetime.datetime.combine((self.startDatetime - datetime.timedelta(self.numberOfDays)).date(), datetime.time(0,0,0))
        strBegTime = begTime.strftime("'%Y-%m-%d %H:%M:%S'")
        '''
        for n in range(self.numberOfDays + 1):
            day = self.startDatetime.date()
            day = day +datetime.timedelta(-n)
            if self.includeWeekends == False:
                if day.weekday() == 5 or day.weekday() == 6:
                    continue
            rawDataKeyFloor = {}
            strDay = day.strftime("'%Y-%m-%d'")
        '''
        for tableName in self.tableNameList:
            predictions = []
            query = "Select a.TIMESTAMP, a.Value from " + tableName + " a"
            query += " WHERE a.TIMESTAMP > " + strBegTime  
            query += " and a.TIMESTAMP < "+  strEndTime + " ORDER BY a.TIMESTAMP ASC"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
            except:
                print "database read failed in SAT, check table name: " + tableName
                return
            for i in range(len(rows)):
                predictions.append((rows[i][0].replace(second = 0, microsecond =0), rows[i][1]))
            for ts, val in predictions:
                if ts.date() not in self.rawDataKeyDayKeyFloor:
                    if ts.date().weekday() == 5 or ts.date().weekday() == 6:
                        if self.includeWeekends == False:
                            continue
                    self.rawDataKeyDayKeyFloor[ts.date()] = {}
                    print "Supply Air Temp Queried and Recieved for date: " + str(ts.date())
                for correspondingFloor in self.floorsKeyTableName[tableName]:
                    if correspondingFloor not in self.rawDataKeyDayKeyFloor[ts.date()]:
                        self.rawDataKeyDayKeyFloor[ts.date()][correspondingFloor] = []
                    #print "added floor " + str(correspondingFloor)
                    if ts.date() == self.startDatetime.date():
                        self.maxTS = ts.replace(second = 0, microsecond =0)
                #print((ts, val))
                    self.rawDataKeyDayKeyFloor[ts.date()][correspondingFloor].append((ts, val))
            
            

        
