class parameterObject():
    def __init__(self, buildingID, floorList, sptPredictionParams, sptParams,
                 satParams, satSPParams, steamPredictionParams,
                 electricityPredictionParams, startupParams, rampdownParams,
                 sptTrajectoryParams):
        self.floorList = floorList
        self.buildingID = buildingID
        self.sptPredictionParams = sptPredictionParams
        self.sptParams = sptParams
        self.satParams = satParams
        self.satSPParams= satSPParams
        self.steamPredictionParams = steamPredictionParams
        self.startupParams = startupParams
        self.electricityPredictionParams = electricityPredictionParams
        self.rampdownParams = rampdownParams
        self.sptTrajectoryParams = sptTrajectoryParams


class parameterObjectLex():
    def __init__(self, buildingID, floorList, sptPredictionParams, sptParams,
                 satParams, ratParams,
                 electricityPredictionParams, startupParams,
                 rampdownParams, sptTrajectoryParams):
        self.floorList = floorList
        self.buildingID = buildingID
        self.sptPredictionParams = sptPredictionParams
        self.sptParams = sptParams
        self.satParams = satParams
        self.ratParams = ratParams
        self.startupParams = startupParams
        self.electricityPredictionParams = electricityPredictionParams
        self.rampdownParams = rampdownParams
        self.sptTrajectoryParams = sptTrajectoryParams


class singleTypeParameterObject():
    def __init__(self):
        pass

