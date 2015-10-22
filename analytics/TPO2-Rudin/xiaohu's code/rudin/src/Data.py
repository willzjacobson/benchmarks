'''
Created on Nov 6, 2012

@author: xiaohu
'''
from datetime import *
import numpy
import math

class Data():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    def __del__(self):
        pass

def ProcessStartUpData(cursor, STARTUP_TABLE, start_date, end_date):
    query='select timestamp from '+STARTUP_TABLE+' where timestamp between '+start_date+' and '+end_date
    cursor.execute(query)
    rows=cursor.fetchall()
    Dataset=[]
    t=Data()
    t.date=rows[0][0].date()
    t.startup1=rows[0][0].time()
    t.startup2=[]
    Dataset.append(t)
    #print(Dataset[0].startup1)
    j=0
    for i in range (1,len(rows)):
        #print 'i=',i
        if rows[i][0].date()==Dataset[j].date:
            Dataset[j].startup2=rows[i][0].time()
        else:
            j=j+1
            t=Data()
            t.startup1=time(rows[i][0].hour,rows[i][0].minute,rows[i][0].second)
            t.startup2=[]
            t.date=rows[i][0].date()
            Dataset.append(t)
    return Dataset

def ProcessSpaceTempData(cursor,table,Dataset,delay,epsilon,season):
    for i in range(0,len(Dataset)):
        #print i
        Dataset[i].space_temp_time=[]
        Dataset[i].space_temp_value=[]
        Dataset[i].endtime=None
        d=datetime.combine(Dataset[i].date,Dataset[i].startup1)
        query='select TimeStamp, Value from '+table+" where datediff(day, '"+str(Dataset[i].date)+"', timestamp)=0 and timestamp > '"+str(d)+"'"
        cursor.execute(query)
        rows=cursor.fetchall()
        #print len(rows), rows
        #print rows[3][0].time()
        for j in range(delay,len(rows)):
            if (season=='winter' and rows[j-1][1]-rows[j][1]>=-epsilon) or (season=='summer' and rows[j-1][1]-rows[j][1]<=epsilon):
                #print 'find', i
                for k in range (delay, j+1):
                    Dataset[i].space_temp_time.append(time(rows[k][0].hour,rows[k][0].minute,rows[k][0].second))
                    Dataset[i].space_temp_value.append(rows[k][1])
                Dataset[i].endtime=time(rows[j][0].hour,rows[j][0].minute,rows[j][0].second)
                break
        #print Dataset[i].space_temp_time,Dataset[i].space_temp_value
    return Dataset

def ProcessCHWTempData(cursor,table,Dataset):
    for i in range(0,len(Dataset)):
        Dataset[i].chw_temp_time=[]
        Dataset[i].chw_temp_value=[]
        d1=datetime.combine(Dataset[i].date,Dataset[i].startup1)
        if Dataset[i].endtime==None:
            continue
        else: d2=datetime.combine(Dataset[i].date,Dataset[i].endtime)
        query='select timestamp, value from '+table+" where datediff(day, '"+str(Dataset[i].date)+"', timestamp)=0 and timestamp between '"+str(d1)+"' and '"+str(d2)+"'"
        #print query
        cursor.execute(query)
        rows=cursor.fetchall()
        for j in range(0,len(rows)):
            Dataset[i].chw_temp_time.append(time(rows[j][0].hour,rows[j][0].minute,rows[j][0].second))
            Dataset[i].chw_temp_value.append(rows[j][1])
        #print Dataset[i].chw_temp_time,Dataset[i].chw_temp_value
    return Dataset

def ProcessValveData(cursor,table,Dataset):
    for i in range(0, len(Dataset)):
        Dataset[i].valve_time=[]
        Dataset[i].valve_value=[]
        d1=datetime.combine(Dataset[i].date,Dataset[i].startup1)
        d2=datetime.combine(Dataset[i].date,Dataset[i].endtime)       
        query='select timestamp, value from '+table+" where datediff(day, '"+str(Dataset[i].date)+"', timestamp)=0 and timestamp between '"+str(d1)+"' and '"+str(d2)+"'"
        cursor.execute(query)
        rows=cursor.fetchall()
        for j in range(0,len(rows)):
            Dataset[i].valve_time.append(time(rows[j][0].hour,rows[j][0].minute,rows[j][0].second))
            Dataset[i].valve_value.append(rows[j][1])
        #print Dataset[i].valve_time,Dataset[i].valve_value
    return Dataset
        
def ProcessPeriTempData(cursor, table, Dataset):
    for i in range(0, len(Dataset)):
        Dataset[i].peri_temp_time=[]
        Dataset[i].peri_temp_value=[]
        d1=datetime.combine(Dataset[i].date,Dataset[i].startup1)
        d2=datetime.combine(Dataset[i].date,Dataset[i].endtime)    
        query='select timestamp, value from '+table+" where datediff(day, '"+str(Dataset[i].date)+"', timestamp)=0 and timestamp between '"+str(d1)+"' and '"+str(d2)+"'"
        cursor.execute(query)
        rows=cursor.fetchall()
        for j in range(0,len(rows)):
            Dataset[i].peri_temp_time.append(time(rows[j][0].hour,rows[j][0].minute,rows[j][0].second))
            Dataset[i].peri_temp_value.append(rows[j][1])
        #print Dataset[i].peri_temp_time,Dataset[i].peri_temp_value
    return Dataset

def CalcCorrelation(Dataset):
    correlation= [[0 for col in range(5)] for row in range(len(Dataset))]
    for i in range(0, len(Dataset)):
        correlation[i][0]=numpy.mean(Dataset[i].chw_temp_value)
        correlation[i][1]=numpy.mean(Dataset[i].valve_value)
        correlation[i][2]=numpy.mean(Dataset[i].peri_temp_value)
        correlation[i][3]=numpy.max(Dataset[i].space_temp_value)-numpy.min(Dataset[i].space_temp_value)
        correlation[i][4]=len(Dataset[i].space_temp_value)
        #print correlation[i]
    return correlation

def CalcT(T0, deltaT, t, RC):
    return T0-deltaT*(1-math.exp(-t/RC))

def calcRC(Dataset, minRC, maxRC, step):
    min_err=float("inf")
    for RC in numpy.arange(minRC, maxRC, step):
        err=0
        #print RC
        for i in range(len(Dataset)):
            for j in range(len(Dataset[i].space_temp_value)):
                if len(Dataset[i].space_temp_value)==1: continue
                err=err+(CalcT(Dataset[i].space_temp_value[0], Dataset[i].space_temp_value[0]-Dataset[i].space_temp_value[-1], j, RC)-Dataset[i].space_temp_value[j])**2
        #print err, RC
        if err<min_err:
            min_err=err
            best_RC=RC
            #print best_RC
            #print err
            
    return best_RC

def calcMape(Dataset, RC):
    mape=[]
    for i in range(len(Dataset)):
        Dataset[i].estimate=[]
        for j in range(len(Dataset[i].space_temp_value)):
            Dataset[i].estimate.append(CalcT(Dataset[i].space_temp_value[0], Dataset[i].space_temp_value[0]-Dataset[i].space_temp_value[-1], j, RC))
            mape.append(abs(Dataset[i].estimate[j]-Dataset[i].space_temp_value[j])/Dataset[i].space_temp_value[j])
    return mape      