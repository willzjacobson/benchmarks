from spaceTemperature_trajectory.score_trajectories.spaceTempTrajectoryScorer import spaceTemperatureTrajectoryScorerPark
import data_tools.dataCollectors as dataCollectors
import data_tools.parkParameters as parkParameters
import data_tools.parameterObject as parameterObject
import sys
import os
import datetime
import pyodbc
import matplotlib.pyplot as plt


def main(argv):
    if argv is None:
        argv = sys.argv

    server='bell.ldeo.columbia.edu'
    db='Rudin_345Park'
    uid='XiaohuLi'
    pwd='Lixiaohu356'
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()

    paramObj = parkParameters.initializeParametersPark()
    now = datetime.datetime.now() + datetime.timedelta(-3)
    now = datetime.datetime.combine(now.date(), datetime.time(23,59))

    relevantHours = (datetime.time(0, 00), datetime.time(23,59)) # we want 24/7 predictions
    scorer = {}
    for i in range(1,9):
        scorer[i] = spaceTemperatureTrajectoryScorerPark(conn, cursor, paramObj, now, i)
        scorer[i].readFromDB()
        scorer[i].autorun()
        
    colors = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow',
          'white', 'black', 'brown', 'Aqua', 'DarkGray', 'DarkKhaki',
          'DarkMagenta', 'Indigo', 'LightCoral', 'LawnGreen', 'Fuchsia',
          'FireBrick', 'deepskyblue', 'Navy', 'OrangeRed', 'PaleVioletRed',
          'Orange', 'YellowGreen']
    plt.hold(True)
    counter = 0
  
    for floor in paramObj.floorList:
        errVals = []
        for i in range(1,9):
            errVals.append(scorer[i].scoreKeyFloor[floor])
        if floor == 5:
            continue
        myPlot = plt.plot([timestep for timestep in range(1,9)], errVals, color = colors[counter], label = str(floor))
        counter+=1
    plt.xlabel('Timestep')
    plt.ylabel('Squared Error')
    plt.title("345 Park Trajectory error -- " + str(now.date()))
    plt.legend()
    plt.savefig('ParkTrajectorySquaredError' + str(now.date()) + ".png")
    

        

if __name__ == '__main__':
	main(sys.argv)



    
