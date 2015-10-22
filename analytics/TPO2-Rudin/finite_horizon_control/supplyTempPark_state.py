from state_cost_base import state_cost_base
from data_tools.dataCollectors import *
# not sure if this is necessary yet...
class supplyTempPark_state(state_cost_base):
    def __init__(self,conn,cursor,paramObj, numberOfDays, startDateTime):
        state_cost_base.__init__(self,conn,cursor,paramObj, numberOfDays, startDateTime)

    def readFromDB(self):
        self.
