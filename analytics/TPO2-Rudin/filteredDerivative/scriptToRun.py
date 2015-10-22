'''
to run the filtered derivative
'''

import matplotlib.pyplot as plt
import pyodbc
import datetime
from filteredDerivative import *

floorList = [2, 5, 13, 18, 20, 24, 32, 38, 40]

trueValsLex = [('Lex560_10thTop', 'AC_11thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_12thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_13thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_14thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_15thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_16thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_17thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_18thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_19thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_20thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_21stFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_22ndFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_10thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_2ndFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_3rdFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_4thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_5thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_6thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_7thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_8thFlBot', 'TxFanStatus'),
('Lex560_10thTop', 'AC_9thFlBot', 'TxFanStatus')]

floorListLex = ['AC_11thFlTop', 'AC_12thFlTop', 'AC_15thFlTop','AC_20thFlTop','AC_2sthFlTop','AC_22ndFlTop','AC_2ndFlTop','AC_5thFlTop', 'AC_9thFlTop']
    
'''
train_start_date = datetime.date(2013,02,02)
train_end_date = datetime.date(2013,02,25)
test_start_date = datetime.date(2013,02,26)
test_end_date = datetime.date(2013,03,8)
predictionDate = datetime.date(2013,03,18)

'''

train_start_date = datetime.date(2013,03,01)
train_end_date = datetime.date(2013,03,8)
test_start_date = datetime.date(2013,03,11)
test_end_date = datetime.date(2013,03,15)
predictionDate = datetime.date(2013,03,18)

'''
server='bell.ldeo.columbia.edu'
db='Rudin_345Park'
uid='XiaohuLi'
pwd='Lixiaohu356'
connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
conn=pyodbc.connect(connString) 
cursor=conn.cursor()
fanList = ['RUDINSERVER_LCP_34E11_S6_STAT', 'RUDINSERVER_LCP_34E11_S5_STAT', 'RUDINSERVER_LCP_34E11_S2_STAT','RUDINSERVER_LCP_34W14_S1_STAT', 'RUDINSERVER_LCP_34W14_S3_STAT', 'RUDINSERVER_LCP_34W14_S4_STAT', 'RUDINSERVER_LCP_9E4_S12_STS', 'RUDINSERVER_LCP_9E4_S7_STS','RUDINSERVER_LCP_9E4_S8_STS','RUDINSERVER_LCP_9W5_S10_STS', 'RUDINSERVER_LCP_9W5_S9_STS']
'''



server='bucky.ldeo.columbia.edu'
db='ContinuumDB'
uid='rudin_db_reader'
pwd='rud1n2012$'
connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
conn=pyodbc.connect(connString) 
cursor=conn.cursor()

populate_dayStart = datetime.date(2013,03,18)
populate_dayEnd = datetime.date(2013,03,22)

up = FilteredDerivativeStartupLex(conn, cursor, floorListLex, train_start_date, train_end_date, test_start_date, test_end_date, predictionDate,windowSize = (1, 5), derivSpace = (2,6), contiguousVals = (2,4), valueTable = trueValsLex, includeWeekends = False, lookForNegs = False, FDtimeTuple = (datetime.time(03,30), datetime.time(07,15)))
#up.commitPredictions_SQL('startup_time_rec', populate_dayStart, populate_dayEnd)
#up.commitTrueVals_SQL('startup_time_actual')
up.commitMinTupFDData_SQL('startup_filteredDerivatives')
#print up.predictDate(predictionDate)
#print up.predictDate(datetime.date(2013,03,19), True)
#up.plotTruthAndPrediction(10)

'''
up = FilteredDerivativeStartupPark(conn, cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, predictionDate,windowSize = (1, 9), derivSpace = (2,10), contiguousVals = (2,6), valueTable = fanList, includeWeekends = False, lookForNegs = False, FDtimeTuple = (datetime.time(03,30), datetime.time(07,15)))
#up.commitPredictions_SQL('startup_time_rec', populate_dayStart, populate_dayEnd)
#up.commitTrueVals_SQL('startup_time_actual')
up.commitMinTupFDData_SQL('startup_filteredDerivatives')
#print up.predictDate(predictionDate)
#print up.predictDate(datetime.date(2013,03,19), True)
up.plotTruthAndPrediction(10)

'''


down = FilteredDerivativeRampdownLex(conn, cursor, floorListLex, train_start_date, train_end_date, test_start_date, test_end_date,predictionDate,windowSize = (5, 17), derivSpace = (4,10), contiguousVals = (3,7), valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00)))
down.commitPredictions_SQL('rampdown_time_rec', populate_dayStart, populate_dayEnd)
down.commitTrueVals_SQL('rampdown_time_actual')
down.commitMinTupFDData_SQL('rampdown_filteredDerivatives')

#down.plotTruthAndPrediction(10)


'''
for n in range(int((populate_dayEnd - populate_dayStart).days +1)):
    day = populate_dayStart + datetime.timedelta(n)
    if day.weekday() == 6 or day.weekday() == 5:
        continue
    print up.predictDate(day, True)
    '''
'''
    query = "insert into startup_time_rec(Run_DateTime, Prediction_DateTime) values ('" + up.timeStamp.strftime("%Y-%m-%d %H:%M") + "', '" + str(up.predictDate(day, False)) +"' )"
    cursor.execute(query)
    conn.commit()
'''
'''
down = FilteredDerivativeRampdown(cursor, floorList, train_start_date, train_end_date, test_start_date, test_end_date, predictionDate,windowSize = (7, 13), derivSpace = (4,10), contiguousVals = 5, valueTable = 'Ramp_Down_Time_DS', includeWeekends = False, lookForNegs = True, FDtimeTuple = (datetime.time(12,30), datetime.time(19,00)))
print app.predictDate(predictionDate)
print app.predictDate(datetime.date(2013,03,19))
app.fdtrainer_fdtester[app.minTup][1].filteredDerivsKeyDay[datetime.date(2013,3,14)].plot(True, True, True, None)
'''

'''
Predictor = FilteredDerivativePredictor(cursor, train_start_date, train_end_date, floorList, windowSize, 4 ,4)

Predictor.fillRegressionWeights()

Tester = FilteredDerivativeTester(cursor, test_start_date, test_end_date, floorList, windowSize, 4 ,4)

Tester.calculatePredictions(Predictor.regressionObject)

for i in range(len(Tester.YActual)):
    print Tester.YActual[i], Tester.YPredicted[i]

for floor in myFilteredDeriv.filteredDerivativeKeyFloor:        
    print str(floor) + ": " + str(myFilteredDeriv.rdTimeValuesKeyFloor[floor])
    if floor == 18 or floor == 24:
        for i in range(len(myFilteredDeriv.filteredDerivativeKeyFloor[floor])):
            print myFilteredDeriv.filteredDerivativeKeyFloor[floor][i]

'''
