## set up parameter objects for Park:
from parameterObject import *
'''
This file will be updated until we have valid entries in the config for
these parameters.

We add a new singleTypeParameterObject(), which is simply and empty/dummy
holder class, to represent the necesarry parameters needed to pair
with the queries made in dataCollectors
'''
def initializeParametersPark():
    ''' General '''
    floorList = [2, 5, 13, 18, 20, 24, 32, 38, 40, 4]
    equipmentNumberKeyFloor = {2:10, 5:12, 13:9, 18:11, 20:4, 24:6, 32:4, 38: 3, 40:5, 4:10}
    quadrantKeyFloor = {2 : 'NW', 5: 'SE', 13: 'SW', 18:'SE', 20:'SW', 24:'SE', 32:'NW', 38:'NW', 40:'NE', 4:'NW'}

    ''' space temperature prediction params '''
    sptPredictionParams = singleTypeParameterObject()
    sptPredictionParams.tableName = "Space_Temperature_Prediction"
    sptPredictionParams.tableFloorDesignator = "Floor"

    ''' space temperature params''' 
    sptParams = singleTypeParameterObject()
    sptTableNameList = []
    sptFloorsKeyTableName = {}
    for floor in floorList:
        tableName = "RUDINSERVER_FL" + str(floor) +"_" + quadrantKeyFloor[floor] + "_SPACETEMP"
        sptTableNameList.append(tableName)
        sptFloorsKeyTableName[tableName] = floor

    sptParams.tableNameList = sptTableNameList
    sptParams.floorsKeyTableName = sptFloorsKeyTableName

    ''' supply air temperature params '''
    satParams = singleTypeParameterObject()
    satTableNameList = []
    satFloorsKeyTableName = {}
    for floor in floorList:
        tableName = "RUDINSERVER_S" + str(equipmentNumberKeyFloor[floor]) + "_SAT"
        satTableNameList.append(tableName)
        if tableName not in satFloorsKeyTableName:
            satFloorsKeyTableName[tableName] = []
            satFloorsKeyTableName[tableName].append(floor)
        else:
            satFloorsKeyTableName[tableName].append(floor)

    satParams.tableNameList = satTableNameList
    satParams.floorsKeyTableName = satFloorsKeyTableName

    ''' supply air temperature set point params '''
    satSPParams = singleTypeParameterObject()
    satSPTableNameList = []
    satSPFloorsKeyTableName = {}
    for floor in floorList:
        tableName = "RUDINSERVER_S" + str(equipmentNumberKeyFloor[floor]) + "_SAT_SP"
        satSPTableNameList.append(tableName)
        if tableName not in satSPFloorsKeyTableName:
            satSPFloorsKeyTableName[tableName] = []
            satSPFloorsKeyTableName[tableName].append(floor)
        else:
            satSPFloorsKeyTableName[tableName].append(floor)

    satSPParams.tableNameList = satSPTableNameList
    satSPParams.floorsKeyTableName = satSPFloorsKeyTableName

    ''' steam prediction params '''
    steamPredictionParams = singleTypeParameterObject()
    steamPredictionParams.tableName = "Steam_Demand_Prediction"

    ''' electricity prediction params '''
    electricityPredictionParams = singleTypeParameterObject()
    electricityPredictionParams.tableName = "Electric_Load_Prediction"

    ''' rampdown params '''
    rampdownParams = singleTypeParameterObject()
    rampdownParams.tableName = "Ramp_Down_Time_DS"

    ''' startup params '''
    startupParams = singleTypeParameterObject()
    startupParams.tableNameList = ['RUDINSERVER_LCP_34E11_S6_STAT', 'RUDINSERVER_LCP_34E11_S5_STAT','RUDINSERVER_LCP_34E11_S2_STAT',
                                 'RUDINSERVER_LCP_34W14_S1_STAT','RUDINSERVER_LCP_34W14_S3_STAT', 'RUDINSERVER_LCP_34W14_S4_STAT',
                                 'RUDINSERVER_LCP_9E4_S12_STS', 'RUDINSERVER_LCP_9E4_S7_STS','RUDINSERVER_LCP_9E4_S8_STS',
                                 'RUDINSERVER_LCP_9W5_S10_STS', 'RUDINSERVER_LCP_9W5_S9_STS']

    ''' space temperature trajectory params '''
    sptTrajectoryParams = singleTypeParameterObject()
    sptTrajectoryParams.tableName = "spaceTemperature_trajectory"
    sptTrajectoryParams.tableFloorDesignator = "Floor"

    ''' _build parameter object '''
    
    paramObj = parameterObject('Park', floorList, sptPredictionParams, sptParams, satParams, satSPParams,
                               steamPredictionParams,electricityPredictionParams, startupParams, rampdownParams,
                               sptTrajectoryParams)
    paramObj.quadrantKeyFloor = quadrantKeyFloor
    paramObj.equipmentNumberKeyFloor = equipmentNumberKeyFloor
    return paramObj
    
    

