'''
Created on Nov 6, 2012

@author: xiaohu
'''
import pyodbc
from Data import *

epsilon=0.5
delay=1
minRC=0.1
maxRC=10
step=0.1
start_date="'2012-11-26'"
test_date="'2012-11-30'"
end_date="'2012-12-10'"
season="summer"
'''start_date="'2012-10-29'"
test_date="'2012-11-20'"
end_date="'2012-11-30'"
season="winter"'''
#FLOOR=[2, 5, 13, 18, 20, 24, 32, 35, 38, 40]
#ZONE=['NE', 'NW', 'SE', 'SW']
FLOOR=[20]
ZONE=['NE']
server='bell.ldeo.columbia.edu'
db='Rudin_345Park'
uid='XiaohuLi'
pwd='Lixiaohu356'
connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
conn=pyodbc.connect(connString) 
cursor=conn.cursor()
for floor in FLOOR:
    for zone in ZONE:
        CHW_TEMP_TABLE='RUDINSERVER_CHLR1_CHWS_TEMP'
        SPACE_TEMP_TABLE='RUDINSERVER_FL'+str(floor)+'_'+zone+'_SPACETEMP'
        if floor>=2 and floor <=8:
            if zone=='NW' or zone=='SW': valve='S10'
            else: valve='S12'
        elif floor>=10 and floor <=19:
            if zone=='NW' or zone=='SW': valve='S9'
            else: valve='S11'
        elif floor>=20 and floor <=33:
            if zone=='NW' or zone=='SW': valve='S4'
            else: valve='S6'
        elif floor>=35 and floor <=44:
            if zone=='NW' or zone=='SW': valve='S3'
            else: valve='S5'
        VALVE_TABLE='RUDINSERVER_'+valve+'_CHW_VLV'
        if valve=='S12': VALVE_TABLE=VALVE_TABLE+'_CMD'
        if zone=='NW' or zone=='NE':
            direction='SOUTH'
        else: direction='NORTH'
        PERIMETER_TEMP_TABLE='RUDINSERVER_FL'+str(floor)+'_'+direction+'_SPACETEMP'
        STARTUP_TABLE='Start_Up_Time'
        Dataset_train=ProcessStartUpData(cursor, STARTUP_TABLE, start_date, test_date)
        Dataset_test=ProcessStartUpData(cursor, STARTUP_TABLE, test_date, end_date)
        #print len(Dataset)
        Dataset_train=ProcessSpaceTempData(cursor,SPACE_TEMP_TABLE,Dataset_train,delay,epsilon,season)
        Dataset_test=ProcessSpaceTempData(cursor,SPACE_TEMP_TABLE,Dataset_test,delay,epsilon,season)
        Dataset_train=ProcessCHWTempData(cursor,CHW_TEMP_TABLE,Dataset_train)
        Dataset_test=ProcessCHWTempData(cursor,CHW_TEMP_TABLE,Dataset_test)
        #Dataset=ProcessValveData(cursor,VALVE_TABLE,Dataset)
        #Dataset=ProcessPeriTempData(cursor, PERIMETER_TEMP_TABLE, Dataset)
        #correlation=CalcCorrelation(Dataset)
        bestRC=calcRC(Dataset_train, minRC, maxRC, step)
        print 'floor', floor, zone, bestRC
        #print bestRC
        mape=calcMape(Dataset_test,bestRC)
        #print floor, zone, 'MAPE:', sum(mape)/len(mape)*100,'%'
        #len_of_test=[]
        #for i in range(len(Dataset_test)):
        #    len_of_test.append(len(Dataset_test[i].space_temp_value))
        #print 'average length', float(sum(len_of_test))/len(len_of_test)
        
        #show the difference between real space temp and estimated space temp
        '''realtemp=[]
        estimatedtemp=[]
        for i in range(len(Dataset_train)):
            Dataset_train[i].estimate=[]
            for j in range(len(Dataset_train[i].space_temp_value)):
                Dataset_train[i].estimate.append(CalcT(Dataset_train[i].space_temp_value[0], numpy.max(Dataset_train[i].space_temp_value)-numpy.min(Dataset_train[i].space_temp_value), j, bestRC))
            realtemp.append(Dataset_train[i].space_temp_value)
            estimatedtemp.append(Dataset_train[i].estimate)
        print 'start to print real temp'
        for i in range(len(realtemp)):
            print 'day ',i
            for j in range(len(realtemp[i])):
                print realtemp[i][j]
        print 'start to print estimated temp'
        for i in range(len(estimatedtemp)):
            print 'day ',i
            for j in range(len(estimatedtemp[i])):
                print estimatedtemp[i][j]'''
        
        #show the correlation between chilled water temp and spacetemp(statistically)
        #print 'start to print daily chilled water temp & spacetemp'
        #for i in range(len(Dataset)):
        #    if len(Dataset[i].chw_temp_value)>0 and len(Dataset[i].space_temp_value)>0:
        #        if Dataset[i].startup2==[]:
        #            print numpy.mean(Dataset[i].chw_temp_value),numpy.max(Dataset[i].space_temp_value)-numpy.min(Dataset[i].space_temp_value)
        #        else:
        #            print numpy.mean(Dataset[i].chw_temp_value),(numpy.max(Dataset[i].space_temp_value)-numpy.min(Dataset[i].space_temp_value))/2
        
        #show the real-time correlation between chilled water temp and spacetemp
        #for d in Dataset:
        #    for i in range(len(d.space_temp_value)-1):
        #        print d.chw_temp_value[i+delay-1], d.space_temp_value[i]    