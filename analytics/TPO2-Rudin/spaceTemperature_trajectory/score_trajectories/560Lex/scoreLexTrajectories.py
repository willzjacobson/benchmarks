from spaceTemperature_trajectory.score_trajectories.spaceTempTrajectoryScorer import spaceTemperatureTrajectoryScorerLex
import data_tools.dataCollectors as dataCollectors
import data_tools.lexParameters as lexParameters
import data_tools.parameterObject as parameterObject
import sys
import os
import datetime
import pyodbc
import matplotlib.pyplot as plt


def main(argv):
    if argv is None:
        argv = sys.argv

    server='bucky.ldeo.columbia.edu'
    db='ContinuumDB'
    uid='rudin_db_reader'
    pwd='rud1n2012$'
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()

    paramObj = lexParameters.initializeParametersLex()
    now = datetime.datetime.now() + datetime.timedelta(0)
    now = datetime.datetime.combine(now.date(), datetime.time(23,59))

    relevantHours = (datetime.time(0, 00), datetime.time(23,59)) # we want 24/7 predictions
    scorer = {}
    for i in range(1,9):
        scorer[i] = spaceTemperatureTrajectoryScorerLex(conn, cursor, paramObj, now, i)
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
    plt.title("560 Lex Trajectory error -- " + str(now.date()))
    plt.legend()
    plt.savefig('LexTrajectorySquaredError' + str(now.date()) + ".png")
    

        

if __name__ == '__main__':
	main(sys.argv)



    
