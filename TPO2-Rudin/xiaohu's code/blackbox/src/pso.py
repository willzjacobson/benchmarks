'''
Created on Nov 17, 2012

@author: xiaohu
'''
from random import *
import math
from svmutil import *
from datetime import *
import pyodbc



def getData(start_date, end_date, CHW_Table, PERI_TEMP_Table, SPACE_TEMP_Table, cursor):
    CHW_DATA=[]
    PERI_TEMP_DATA=[]
    SPACE_TEMP_DATA=[]
    SPACE_TEMP_WEEK=[]
    PERI_TEMP_WEEK=[]
    date1=datetime.strptime(start_date,'%Y-%m-%d')
    date2=datetime.strptime(end_date,'%Y-%m-%d')
    delta=timedelta(days=1)
    date3=date1+delta
    while date3<=date2:
        d1=datetime.strftime(date1,'%Y-%m-%d')
        d2=datetime.strftime(date3,'%Y-%m-%d')
        d1_week=datetime.strftime(date1+timedelta(weeks=-1),'%Y-%m-%d')
        d2_week=datetime.strftime(date3+timedelta(weeks=-1),'%Y-%m-%d')
        query_chw="select value from {0} where datepart(hour,timestamp) between 7 and 19 and datepart(weekday,timestamp) between 2 and 6 and timestamp between '{1}' and '{2}'".format(CHW_Table, d1, d2)
        query_peri="select value from {0} where datepart(hour,timestamp) between 7 and 19 and datepart(weekday,timestamp) between 2 and 6 and timestamp between '{1}' and '{2}'".format(PERI_TEMP_Table, d1, d2)
        query_space="select value from {0} where datepart(hour,timestamp) between 7 and 19 and datepart(weekday,timestamp) between 2 and 6 and timestamp between '{1}' and '{2}'".format(SPACE_TEMP_Table, d1, d2)
        query_space_week="select value from {0} where datepart(hour,timestamp) between 7 and 19 and datepart(weekday,timestamp) between 2 and 6 and timestamp between '{1}' and '{2}'".format(SPACE_TEMP_Table, d1_week, d2_week)
        query_peri_week="select value from {0} where datepart(hour,timestamp) between 7 and 19 and datepart(weekday,timestamp) between 2 and 6 and timestamp between '{1}' and '{2}'".format(PERI_TEMP_Table, d1_week, d2_week)
        cursor.execute(query_chw)
        CHW_DATA.append(cursor.fetchall())
        cursor.execute(query_peri)
        PERI_TEMP_DATA.append(cursor.fetchall())
        cursor.execute(query_space)
        SPACE_TEMP_DATA.append(cursor.fetchall())
        cursor.execute(query_space_week)
        SPACE_TEMP_WEEK.append(cursor.fetchall())
        cursor.execute(query_peri_week)
        PERI_TEMP_WEEK.append(cursor.fetchall())
        date1=date3
        date3=date1+delta
    return CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK

def Randomize_particle(alpha_min, alpha_max, t_min, t_max,c_min,c_max):
    particle=[]
    for i in range(0,5):
        particle.append(uniform(alpha_min, alpha_max))
    for i in range(0,5):
        if i==2:
            particle.append(randint(max(t_min,1),max(t_max,1)))
        else:
            particle.append(randint(t_min, t_max))
    particle.append(uniform(c_min, c_max))
    #particle.append(0)
    return particle

def Randomize_velocity(v_alpha_min, v_alpha_max, v_t_min, v_t_max, v_c_min, v_c_max):
    velocity=[]
    for i in range(0,5):
        velocity.append(uniform(v_alpha_min, v_alpha_max))
    for i in range(0,5):
        velocity.append(uniform(v_t_min, v_t_max))
    velocity.append(uniform(v_c_min, v_c_max))
    return velocity    

def fitness(particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK):
    err=0
    max_lag=max(particle[5],particle[6],particle[7],particle[8],particle[9])
    for i in range(len(CHW_DATA)):
        for j in range(max_lag, min(len(CHW_DATA[i]),len(SPACE_TEMP_WEEK[i]))):
            err=err+float(i)/len(CHW_DATA)*(SPACE_TEMP_DATA[i][j][0]-calc(particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK, i, j))**2
            #print i,j
    return err

def calc(particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK, i, j):
    return particle[0]*CHW_DATA[i][j-particle[5]][0]+particle[1]*CHW_DATA[i][j-particle[6]][0]+particle[2]*SPACE_TEMP_WEEK[i][j-particle[7]][0]+particle[3]*PERI_TEMP_WEEK[i][j-particle[8]][0]+particle[4]*PERI_TEMP_DATA[i][j-particle[9]][0]+particle[10]

def calc_occ(particle, CHW_DATA_TEST, PERI_TEMP_DATA_TEST, SPACE_TEMP_WEEK_TEST, PERI_TEMP_WEEK_TEST, i, j):
    return particle[2]*SPACE_TEMP_WEEK_TEST[i][j-particle[7]][0]+particle[3]*PERI_TEMP_WEEK_TEST[i][j-particle[8]][0]
    
    
def calc_v(v,w,iter,max_iter,c1,Pbest_particle,particle,c2,Gbest_particle, v_alpha_min, v_alpha_max, v_t_min, v_t_max, v_c_min, v_c_max):
    rand1=uniform(0,1)
    rand2=uniform(0,1)
    for i in range(len(v)):
        #v[i]=w*(0.2+0.8*(max_iter-iter)/max_iter)*v[i]+c1*rand1*(Pbest_particle[i]-particle[i])+c2*rand2*(Gbest_particle[i]-particle[i])
        v[i]=w*v[i]+c1*rand1*(Pbest_particle[i]-particle[i])+c2*rand2*(Gbest_particle[i]-particle[i])
    for i in range(0,5):
        if v[i]<v_alpha_min:
            v[i]=v_alpha_min
        if v[i]>v_alpha_max:
            v[i]=v_alpha_max
    for i in range(5,10):
        v[i]=int(v[i])
        if v[i]<v_t_min:
            v[i]=v_t_min
        if v[i]>v_t_max:
            v[i]=v_t_max
    if v[10]<v_c_min:
        v[10]=v_c_min
    if v[10]>v_c_max:
        v[10]=v_c_max   
         
    return v

def update(v,particle,alpha_min, alpha_max, t_min, t_max, c_min, c_max):
    for i in range(len(v)):
        particle[i]=particle[i]+v[i]
    for i in range(0,5):
        if particle[i]<alpha_min:
            particle[i]=alpha_min
        if particle[i]>alpha_max:
            particle[i]=alpha_max
    for i in range(5,10):
        particle[i]=int(particle[i])
        if particle[i]<t_min:
            particle[i]=t_min
        if particle[i]>t_max:
            particle[i]=t_max
    if particle[10]<c_min:
        particle[10]=c_min
    if particle[10]>c_max:
        particle[10]=c_max
    #if particle[8]!=particle[7]:
    #    particle[8]=particle[7]
    return particle

def svm_data(particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK):
    max_lag=max(particle[5],particle[6],particle[7],particle[8],particle[9])
    x=[]
    y=[]
    for i in range(len(CHW_DATA)):
        for j in range(max_lag, min(len(CHW_DATA[i]),len(SPACE_TEMP_WEEK[i]))):
            xx=[]
            xx.append(CHW_DATA[i][j-particle[5]][0])
            xx.append(CHW_DATA[i][j-particle[6]][0])
            xx.append(SPACE_TEMP_WEEK[i][j-particle[7]][0])
            xx.append(PERI_TEMP_WEEK[i][j-particle[8]][0])
            xx.append(PERI_TEMP_DATA[i][j-particle[9]][0])
            x.append(xx)
            y.append(SPACE_TEMP_DATA[i][j][0])
    return y,x
