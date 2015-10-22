

class state_cost_base():
    def __init__(self, conn, cursor, paramObj, numberOfDays, startDatetime):
        self.conn = conn
        self.cursor = cursor
        self.paramObj = paramObj
        self.numberOfDays = numberOfDays
        self.startDatetime = startDatetime
        self.gp = None

    def readFromDB(self):
        pass

    def matrixify(self):
        pass

    def __trainGP(self):
        pass

    def predictGP(self, xVals):
        pass


    def generateSinglePointDataFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            for floor in dataDictKeyDateKeyFloor[day]:
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    time = ts.time()
                    date = ts.date()
                    singlePointDataKeyFloorKeyTS[floor][ts] = value
        self.xListFloorData.append(singlePointDataKeyFloorKeyTS)


    def generateSinglePointDataNoFloor(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            for ts, value in dataDictKeyDate[day]:
                time = ts.time()
                date = ts.date()
                singlePointDataKeyTS[ts] = value
        self.xListNoFloorData.append(singlePointDataKeyTS)


    def state_populateDPListFloorData(self, dataDictKeyDateKeyFloor):
        singlePointDataKeyFloorKeyTS = {}
        for day in dataDictKeyDateKeyFloor:
            for floor in dataDictKeyDateKeyFloor[day]:
                if floor not in singlePointDataKeyFloorKeyTS:
                    singlePointDataKeyFloorKeyTS[floor] = {}
                for ts, value in dataDictKeyDateKeyFloor[day][floor]:
                    time = ts.time()
                    date = ts.date()
                    singlePointDataKeyFloorKeyTS[floor][ts] = value
        self.DPListFloorData.append(singlePointDataKeyFloorKeyTS)


    def state_populateDPListNoFloorData(self, dataDictKeyDate):
        singlePointDataKeyTS = {}
        for day in dataDictKeyDate:
            for ts, value in dataDictKeyDate[day]:
                time = ts.time()
                date = ts.date()
                singlePointDataKeyTS[ts] = value
        self.DPListNoFloorData.append(singlePointDataKeyTS)

    def generateHourData(self):
        if len(self.xListNoFloorData) == 0:
            print "Please run other covariate generation firstbefore running this function"
            return
        hourData = {}
        dataList = self.xListNoFloorData[0]
        for timestamp in dataList:
            hourData[timestamp] = timestamp.hour
        self.xListNoFloorData.append(hourData)
