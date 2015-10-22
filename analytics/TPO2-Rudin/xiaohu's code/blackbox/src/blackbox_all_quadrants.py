'''
Created on Nov 17, 2012

@author: xiaohu
'''
from pso import *
from datetime import *
import pyodbc
from svmutil import *

FLOOR=[2, 5, 13, 18, 20, 24, 32, 35, 38, 40]
ZONE=['NE', 'NW', 'SE', 'SW']
N_of_Particles=100
c1=2
c2=2
w=1
max_iter=200
alpha_min=-2
alpha_max=2
t_min=0
t_max=4
c_min=-100
c_max=100
v_alpha_min=-0.05
v_alpha_max=0.05
v_t_min=-2
v_t_max=2
v_c_min=-10
v_c_max=10
start_date='2012-08-01'
end_date='2012-09-01'
test_end_date='2012-09-10'
for floor in FLOOR:
    for zone in ZONE:
        particle=[]
        v=[]
        for i in range(0,N_of_Particles):
            particle.append(Randomize_particle(alpha_min, alpha_max, t_min, t_max,c_min,c_max))
            v.append(Randomize_velocity(v_alpha_min, v_alpha_max, v_t_min, v_t_max,v_c_min,v_c_max))
        server='bell.ldeo.columbia.edu'
        db='Rudin_345Park'
        uid='XiaohuLi'
        pwd='Lixiaohu356'
        connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
        conn=pyodbc.connect(connString) 
        cursor=conn.cursor()
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
        CHW_Table='RUDINSERVER_'+valve+'_SAT'
        #CHW_Table='RUDINSERVER_CHLR1_CHWS_TEMP'
        if floor<=20:
            PERI_TEMP_Table='RUDINSERVER_INT_9_OAT'
        else:
            PERI_TEMP_Table='RUDINSERVER_INT_34_OAT'
        SPACE_TEMP_Table='RUDINSERVER_FL'+str(floor)+'_'+zone+'_SPACETEMP'
        CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK=getData(start_date, end_date, CHW_Table, PERI_TEMP_Table, SPACE_TEMP_Table, cursor)
        CHW_DATA_TEST, PERI_TEMP_DATA_TEST, SPACE_TEMP_DATA_TEST, SPACE_TEMP_WEEK_TEST, PERI_TEMP_WEEK_TEST=getData(end_date, test_end_date, CHW_Table, PERI_TEMP_Table, SPACE_TEMP_Table, cursor)
        
        Gbest=float("inf")
        Pbest=[float("inf")]*N_of_Particles
        Gbest_particle=particle[0][:]
        Pbest_particle=particle[:]
        history=[]
        for iter in range(max_iter):
            for n in range(N_of_Particles):
                err=fitness(particle[n], CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK)
                if err<Pbest[n]:
                    Pbest[n]=err
                    Pbest_particle[n]=particle[n][:]
                    if err<Gbest:
                        Gbest=err
                        Gbest_particle=particle[n][:]
                        #print 'Gbest changed'
                        #print 'new gbest:',fitness(Gbest_particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA)
                        #print 'new gbest_value:',Gbest_particle
            #print Gbest_particle
            for n in range(N_of_Particles):
                v[n]=calc_v(v[n],w,iter,max_iter,c1,Pbest_particle[n],particle[n],c2,Gbest_particle, v_alpha_min, v_alpha_max, v_t_min, v_t_max, v_c_min, v_c_max)
                particle[n]=update(v[n],particle[n],alpha_min, alpha_max, t_min, t_max, c_min, c_max)
            #print iter, Gbest, Gbest_particle
            history.append(Gbest)
        #print Gbest_particle   
        #print fitness(Gbest_particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK)
        param='-s 4 -t 2 -q -c 10'
        y_train,x_train=svm_data(Gbest_particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK)
        y_test,x_test=svm_data(Gbest_particle, CHW_DATA_TEST, PERI_TEMP_DATA_TEST, SPACE_TEMP_DATA_TEST, SPACE_TEMP_WEEK_TEST, PERI_TEMP_WEEK_TEST)
        model=svm_train(svm_problem(y_train,x_train), param)
        label,acc,val=svm_predict(y_test,x_test,model)
        err_svm=0
        for i in range(len(y_test)):
            err_svm+=abs(y_test[i]-label[i])/label[i]
        max_lag=max(Gbest_particle[5],Gbest_particle[6],Gbest_particle[7],Gbest_particle[8],Gbest_particle[9])
        #show the model applied to the train data
        #for i in range(len(CHW_DATA)):
        #    for j in range(max_lag, min(len(CHW_DATA[i]),len(SPACE_TEMP_WEEK[i]))):
        #        print SPACE_TEMP_DATA[i][j][0],calc(Gbest_particle, CHW_DATA, PERI_TEMP_DATA, SPACE_TEMP_WEEK, PERI_TEMP_WEEK, i, j)
        #show the model applied to the test data
        #print '*********************************************************'
        err_pso=0
        for i in range(len(CHW_DATA_TEST)):
            for j in range(max_lag, min(len(CHW_DATA_TEST[i]),len(SPACE_TEMP_WEEK_TEST[i]))):
                err_pso+=abs(SPACE_TEMP_DATA_TEST[i][j][0]-calc(Gbest_particle, CHW_DATA_TEST, PERI_TEMP_DATA_TEST, SPACE_TEMP_WEEK_TEST, PERI_TEMP_WEEK_TEST, i, j))/SPACE_TEMP_DATA_TEST[i][j][0]
        print floor, zone, 'svm:', err_svm, 'pso:', err_pso