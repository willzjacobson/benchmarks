## set up parameter objects for Lex:
from parameterObject import *
from configParser import *
'''
This file will be updated until we have valid entries in the config for
these parameters.

We add a new singleTypeParameterObject(), which is simply and empty/dummy
holder class, to represent the necesarry parameters needed to pair
with the queries made in dataCollectors
'''
def initializeParametersLex(configFile, configKey):
    # configFile = 'D:/Rudin/data_tools/config_master.py'
    #configKey = '560_Lex_Params'
    cParser = paramConfigParser(configFile, configKey)

    floorList = cParser.floorList()
    # same order as above
    floorListKeyFloor = cParser.floorListKeyFloor()

    #floorList = ["'F11'", "'F12'", "'F15'","'F20'","'F21'","'F22'","'F02'","'F05'","'F09'"]
    #floorListKeyFloor = {"'F02'":["'F02'"], "'F05'":["'F05'"],"'F09'":["'F09'"], "'F11'":["'F11'"],
    #                     "'F12'":["'F12'"], "'F15'":["'F15'"], "'F20'":["'F20'"], "'F21'":["'F21'"], "'F22'":["'F22'"]}
						 
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
    sptPredictionParams.tableName = cParser.sptPredictionTableName()
    sptPredictionParams.tableFloorDesignator = cParser.sptPredictionTableFloorDesignator()
    #sptPredictionParams.tableName = "Space_Temp_NewFloor"
    #sptPredictionParams.tableFloorDesignator = "FLOOR"

    ''' space temperature params''' 
    sptParams = singleTypeParameterObject()
    sptParams.tableName = cParser.sptTableName()
    sptParams.equalityConstraintList = cParser.sptEqualityConstraintList()
    #sptParams.tableName = "[560---------002BMSHVATEMSPA---VAL001]"
    #sptParams.equalityConstraintList = ['FLOOR']
    sptParams.constraintValListKeyFloor = floorListKeyFloor

    ''' supply air temperature params '''
    satParams = singleTypeParameterObject()
    satParams.tableName = cParser.satTableName()
    satParams.equalityConstraintList = cParser.satEqualityConstraintList()
    #satParams.tableName = "[560---------002BMSHVAFANSAT---VAL001]"
    #satParams.equalityConstraintList = ['FLOOR']
    satParams.constraintValListKeyFloor = floorListKeyFloor

    ''' return air temperature params '''
    ratParams = singleTypeParameterObject()
    ratParams.tableName = cParser.ratTableName()
    ratParams.equalityConstraintList = cParser.ratEqualityConstraintList()
    #ratParams.tableName = "[560---------002BMSHVAFANRAT---VAL001]"
    #ratParams.equalityConstraintList = ['FLOOR']
    ratParams.constraintValListKeyFloor = floorListKeyFloor

    ''' rampdown params '''
    rampdownParams = singleTypeParameterObject()
    rampdownParams.tableName = cParser.rampDownTableName()
    #rampdownParams.tableName = "Ramp_Down_Time_DS"

    ''' electricity prediction params '''
    electricityPredictionParams = singleTypeParameterObject()
    electricityPredictionParams.tableName = cParser.electricityPredictionTableName()
	#electricityPredictionParams.tableName = "[560---------000TPOFORELECON001---001]"

    ''' startup params '''
    startupParams = singleTypeParameterObject()
    startupParams.tableName = cParser.startupTableName()
    startupParams.equalityConstraintList = cParser.startupEqualityConstraintList()
    #startupParams.tableName = "[560---------002BMSHVAFAN------VAL001]"
    #startupParams.equalityConstraintList = ['FLOOR']
    startupParams.constraintValListKeyFloor = startupFloorListKeyFloor


    ''' space temperature trajectory params '''
    sptTrajectoryParams = singleTypeParameterObject()
    sptTrajectoryParams.tableName = cParser.sptTrajectoryTableName()
    sptTrajectoryParams.tableFloorDesignator = cParser.sptTrajectoryTableFloorDesignator()
    #sptTrajectoryParams.tableName = "spaceTemperature_trajectory"
    #sptTrajectoryParams.tableFloorDesignator = "Floor"

    ''' weather observation history params '''
    weatherObsParams = singleTypeParameterObject()
    weatherObsParams.tableName = cParser.weatherObsTableName()

    ''' weather hourly forecast params'''
    weatherHourParams = singleTypeParameterObject()
    weatherHourParams.tableName = cParser.weatherHourTableName()

    ''' occupancy params '''
    occupancyParams = singleTypeParameterObject()
    occupancyParams.tableName = cParser.occupancyTableName()

    ''' _build parameter object '''
    
    paramObj = parameterObjectLex('Lex', floorList, sptPredictionParams, sptParams, satParams, ratParams,
                                electricityPredictionParams, startupParams, rampdownParams, sptTrajectoryParams)
    paramObj.weatherObsParams = weatherObsParams
    paramObj.weatherHourParams = weatherHourParams
    paramObj.occupancyParams = occupancyParams
    return paramObj
    
    

