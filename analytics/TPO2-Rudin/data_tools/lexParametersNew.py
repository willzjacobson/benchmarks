## set up parameter objects for Lex:
from parameterObjectNew import *
'''
This file will be updated until we have valid entries in the config for
these parameters.

We add a new singleTypeParameterObject(), which is simply and empty/dummy
holder class, to represent the necesarry parameters needed to pair
with the queries made in dataCollectors
'''
def initializeParametersLex():
    floorList = ["'F11'", "'F12'", "'F15'","'F20'","'F21'","'F22'","'F02'","'F05'","'F09'"]
    floorListKeyFloor = {"'F02'":["'F02'"], "'F05'":["'F05'"],"'F09'":["'F09'"], "'F11'":["'F11'"],
                         "'F12'":["'F12'"], "'F15'":["'F15'"], "'F20'":["'F20'"], "'F21'":["'F21'"], "'F22'":["'F22'"]}
    startupFloorList = []
    for i in range(2,23):
        if i < 10:
            startupFloorList.append("'F0"+ str(i) + "'")
        else:
            startupFloorList.append("'F" + str(i) + "'")
    startupFloorListKeyFloor = {}
    for floor in startupFloorList:
        startupFloorListKeyFloor[floor] = [floor]


    ''' space temperature prediction params '''
    sptPredictionParams = singleTypeParameterObject()
    sptPredictionParams.tableName = "Space_Temp_NewFloor"
    sptPredictionParams.tableFloorDesignator = "FLOOR"

    ''' space temperature params''' 
    sptParams = singleTypeParameterObject()
    sptParams.tableName = "[560---------002BMSHVATEMSPA---VAL001]"
    sptParams.equalityConstraintList = ['FLOOR']
    sptParams.constraintValListKeyFloor = floorListKeyFloor

    ''' supply air temperature params '''
    satParams = singleTypeParameterObject()
    satParams.tableName = "[560---------002BMSHVAFANSAT---VAL001]"
    satParams.equalityConstraintList = ['FLOOR']
    satParams.constraintValListKeyFloor = floorListKeyFloor

    ''' return air temperature params '''
    ratParams = singleTypeParameterObject()
    ratParams.tableName = "[560---------002BMSHVAFANRAT---VAL001]"
    ratParams.equalityConstraintList = ['FLOOR']
    ratParams.constraintValListKeyFloor = floorListKeyFloor

    ''' rampdown params '''
    rampdownParams = singleTypeParameterObject()
    rampdownParams.tableName = "Ramp_Down_Time_DS"

    ''' electricity prediction params '''
    electricityPredictionParams = singleTypeParameterObject()
    electricityPredictionParams.tableName = "[560---------000TPOFORELECON001---001]"

    ''' startup params '''
    startupParams = singleTypeParameterObject()
    startupParams.tableName = "[560---------002BMSHVAFAN------VAL001]"
    startupParams.equalityConstraintList = ['FLOOR']
    startupParams.constraintValListKeyFloor = startupFloorListKeyFloor


    ''' space temperature trajectory params '''
    sptTrajectoryParams = singleTypeParameterObject()
    sptTrajectoryParams.tableName = "spaceTemperature_trajectory"
    sptTrajectoryParams.tableFloorDesignator = "Floor"

    ''' build parameter object '''
    
    paramObj = parameterObjectLex('Lex', floorList, sptPredictionParams, sptParams, satParams, ratParams,
                                electricityPredictionParams, startupParams, rampdownParams, sptTrajectoryParams)
    return paramObj
    
    

