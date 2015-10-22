from rpy2 import robjects
import state_cost_base
import spaceTempPark_state
import steamPark_cost
from rpy2.robjects.packages import importr

class gpdp():
    def __init__(self, state_obj, cost_obj, horizon, k = 2):
        self.state_obj = state_obj
        self.k = k
        self.cost_obj = cost_obj
        self.horizon = horizon
        self.paramObj = state_obj.paramObj
        self.gptk = importr("gptk")

    def getDPMatrices(self):
        self.state_obj.DPMatrixify(self.horizon)


    def gpdp(self):
        self.memoizedPred = {} # key (floor, currentTemp, suggestedControl, DPMat..., ...)
        self.memoizedCost = {} # key (vector of input values)
        self.memoizedPredKeyHorizon
        for floor in self.paramObj.floorList:
            DPMat = self.state_obj.DPMats[floor]
            self.state_obj.loadGP()
            predTemp_predCost_controlValsKeyHorizon = {} # temperature values predicted, cost predicted, and control to get there
            for n in range(horizon):
                if n == 0:
                    predTemp_predSteam_controlValsKeyHorizon[n] = [(DPMat[0][0], cost_obj.getFinalRecCost, DPMat[0][1])]
                else:
                    predTemp_predSteam_controlValsKeyHorizon[n] = []
                #track all other floor temps and their control lever settings
                currentState = {}
                for floor_inner in self.paramObj.floorList:
                    if floor_inner == floor:
                        continue
                    DPMat_inner = self.state_obj.DPMats[floor_inner]
                    if DPMat_inner[n][0] != -1:
                        currentState[floor_inner] = [DPMat_inner[n][0], DPMat_inner[n][1]]
                    else:
                        currentState[floor_inner] = [DPMat_inner[0][0], DPMat_inner[0][1]]
                for state in range(60,77):
                    for temp, steam, control in predTemp_predSteam_controlValsKeyHorizon[n]:
                        # find next state temperatures
                        xVals = [temp,state, DPMat[n][2], DPMat[n][3]]
                        if (floor, temp,state, DPMat[n][2], DPMat[n][3]) in self.memoizedPred:
                            predTemp = self.memoizedPred[(floor, temp,state, DPMat[n][2], DPMat[n][3])]
                        else:
                            xVals_r = robjects.IntVector(xVals)
                            predTemp = self.state_obj.predictGP(floor, xVals_r)[0][0]
                            self.memoizedPred[(floor, temp,state, DPMat[n][2], DPMat[n][3])] = predTemp
                        predTemp_predSteam_controlValsKeyHorizon[n+1].append((predTemp, state))
                        # find this state's cost
                        vec_r, vec = makeCostQueryVector(steam, temp, control,floor,currentState)
                        if (vec) in self.memoizedCost:
                            predCost = self.memoizedCost[(vec)] # fixed. THIS IS WRONG< because as the temps change, this wont update correctl.
                        else:
                            predSteam = self.cost_obj.predictGP(vec_r)[0][0]
                            predCost = self.costFunction(temp, predSteam)
                            self.memoizedCost[(vec]) = predCost

    def costFunction(self, predTemp, predSteam):
        return(predSteam + self.k * (predTemp - 77)**2 * (predTemp>77) + self.k * (predTemp-73)**2 * (predTemp<73))
        
                        
                        
    def makeCostQueryVector(self, predSteam, predTemp, control, currentFloor, currentState):
        vec = [predSteam]
        for floor in self.paramObj.floorList:
            if floor != currentFloor:
                vec.extend(currentState[floor])
            else:
                vec.extend([predTemp, control])
        vec_r = robjects.IntVector(vec)
        return (vec_r, vec)
            
            
        
