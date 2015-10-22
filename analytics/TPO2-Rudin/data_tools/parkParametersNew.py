## set up parameter objects for Park:
from parameterObject import *
'''
This file will be updated until we have valid entries in the config for
these parameters.

We add a new singleTypeParameterObject(), which is simply and empty/dummy
holder class, to represent the necessary parameters needed to pair
with the queries made in dataCollectors
'''
def initializeParametersPark():
    ''' General '''
    floorList = ["'F02'", "'F05'","'F13'", "'F18'", "'F20'", "'F24'", "'F32'", "'F38'", "'F40'"]
    floorListKeyFloor = {"'F02'":["'F02'"], "'F05'":["'F05'"],"'F13'":["'F13'"], "'F18'":["'F18'"], "'F20'":["'F20'"], "'F24'":["'F24'"], "'F32'":["'F32'"], "'F38'":["'F38'"], "'F40'":["'F40'"]}
    equipmentNumberKeyFloor = {"'F02'":["'010'"], "'F05'":["'012'"], "'F13'":["'009'"], "'F18'":["'011'"], "'F20'":["'004'"], "'F24'":["'006'"], "'F32'":["'004'"], "'F38'": ["'003'"], "'F40'":["'005'"]}
    quadrantKeyFloor = {"'F02'" : ["'CNW'"], "'F05'": ["'CSE'"], "'F13'": ["'CSW'"], "'F18'":["'CSE'"], "'F20'":["'CSW'"], "'F24'":["'CSE'"], "'F32'":["'CNW'"], "'F38'":["'CNW'"], "'F40'":["'CNE'"]}

    ''' space temperature prediction params '''
    sptPredictionParams = singleTypeParameterObject()
    sptPredictionParams.tableName = "space_temp_comp"
    sptPredictionParams.tableFloorDesignator = "Floor"

    ''' space temperature params''' 
    sptParams = singleTypeParameterObject()
    sptParams.tableName = '[345---------001BMSHVATEMSPA---VAL001]'
    sptParams.equalityConstraintList = ['FLOOR', 'QUADRANT']
    sptParams.constraintValListKeyFloor = {}
    for floor in equipmentNumberKeyFloor:
        if floor not in sptParams.constraintValListKeyFloor:
            sptParams.constraintValListKeyFloor[floor] = []
        sptParams.constraintValListKeyFloor[floor].append(floorListKeyFloor[floor][0])
        sptParams.constraintValListKeyFloor[floor].append(quadrantKeyFloor[floor][0])


    ''' supply air temperature params '''
    satParams = singleTypeParameterObject()
    satParams.tableName = '[345---------001BMSHVAFANSAT---VAL001]'
    satParams.equalityConstraintList = ['EQUIPMENT_NO']
    satParams.constraintValListKeyFloor = equipmentNumberKeyFloor

    ''' supply air temperature set point params '''
    satSPParams = singleTypeParameterObject()
    satSPParams.tableName = '[345---------001BMSHVAFANSAT---SPV001]'
    satSPParams.equalityConstraintList = ['EQUIPMENT_NO']
    satSPParams.constraintValListKeyFloor = equipmentNumberKeyFloor

    ''' steam prediction params '''
    steamPredictionParams = singleTypeParameterObject()
    steamPredictionParams.tableName = "[345---------000TPOFORSTECON001---001]"

    ''' electricity prediction params '''
    electricityPredictionParams = singleTypeParameterObject()
    electricityPredictionParams.tableName = "[345---------000TPOFORELECON001---001]"

    ''' rampdown params '''
    rampdownParams = singleTypeParameterObject()
    rampdownParams.tableName = "Ramp_Down_Time_DS"

    ''' startup params '''
    startupParams = singleTypeParameterObject()
    startupParams.tableNameList = ['[345---------001BMSHVAPFALCP---VAL001]', '[345---------001BMSHVAFANLCP---VAL001]']
    startupParams.equalityConstraintList = ['EQUIPMENT_NO']
    startupParams.constraintValListKeyTable = {'[345---------001BMSHVAPFALCP---VAL001]': ["'002'","'008'","'001'", "'007'"],
                                              '[345---------001BMSHVAFANLCP---VAL001]': ["'010'", "'005'", "'003'", "'004'", "'009'", "'006'", "'011'"] }

    ''' space temperature trajectory params '''
    sptTrajectoryParams = singleTypeParameterObject()
    sptTrajectoryParams.tableName = "spaceTemperature_trajectory"
    sptTrajectoryParams.tableFloorDesignator = "Floor"

    ''' build parameter object '''
    
    paramObj = parameterObject('Park', floorList, sptPredictionParams, sptParams, satParams, satSPParams,
                               steamPredictionParams,electricityPredictionParams, startupParams, rampdownParams,
                               sptTrajectoryParams)
    paramObj.quadrantKeyFloor = quadrantKeyFloor
    paramObj.equipmentNumberKeyFloor = equipmentNumberKeyFloor
    return paramObj
    
    

