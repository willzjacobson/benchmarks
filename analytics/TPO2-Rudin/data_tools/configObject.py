import cfgparse
import datetime

class dummy():
        def __init__(self):
                return

class configObject():
        
        def __init__(self, ConfigFileName, ConfigFileKey):
                # these are the default build instructions for TPO BETA release 2's recommendation layer.  All Buildings should buil their config files
                # to be consistent with the formatting paradigm implied by this builder
                self.cparser = cfgparse.ConfigParser()
                self.cparser.add_file(ConfigFileName)
                self.ConfigFileKey = ConfigFileKey;

                # General building info
                self.cparser.add_option('building_floors', dest='floorList', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('floor_quadrants', dest='quadrantList', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('floor_equipments', dest='equipmentsList', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('building_open_hour', dest='buildingOpenHour', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('building_close_hour', dest = 'buildingCloseHour', type = 'string', keys = self.ConfigFileKey)
                self.cparser.add_option('floor_zones', dest = 'zoneList', type='string', keys=self.ConfigFileKey)

                #DB Info
                self.cparser.add_option('SERVER', dest='server', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('DB', dest='db', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('UID', dest='uid', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('PWD', dest='pwd', type='string', keys=self.ConfigFileKey)
                # spt prediction
                self.cparser.add_option('spt_prediction_table_name', dest='sptPredictionTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_prediction_table_floor_designator', dest='sptPredictionTableFloorDesignator', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_prediction_has_quadrants', dest = 'sptPredictionHasQuadrants', type = 'string', keys = self.ConfigFileKey)
                # spt	
                self.cparser.add_option('spt_table_name', dest='sptTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_equality_constraint_list', dest='sptEqualityConstraintList', type='string', keys=self.ConfigFileKey)
                #sat
                self.cparser.add_option('sat_table_name', dest='satTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('sat_equality_constraint_list', dest='satEqualityConstraintList', type='string', keys=self.ConfigFileKey)
                # sat Setpoint
                self.cparser.add_option('satS_table_name', dest='satSTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('satS_equality_constraint_list', dest='satSEqualityConstraintList', type='string', keys=self.ConfigFileKey)
                # steam prediction
                self.cparser.add_option('steam_prediction_table_name', dest='steamPredictionTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('has_steam_supply', dest = 'hasSteamSupply', type = 'string', keys = self.ConfigFileKey)
                # electricity prediction
                self.cparser.add_option('elec_prediction_table_name', dest='electricityPredictionTableName', type='string', keys=self.ConfigFileKey)
                #ramp down
                self.cparser.add_option('ramp_down_table_name', dest='rampDownTableName', type='string', keys=self.ConfigFileKey)
                #startup
                self.cparser.add_option('startup_table_name', dest='startupTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('startup_equality_constraint_list', dest='startupEqualityConstraintList', type='string', keys=self.ConfigFileKey)
                #rat 
                self.cparser.add_option('rat_table_name', dest='ratTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('rat_equality_constraint_list', dest='ratEqualityConstraintList', type='string', keys=self.ConfigFileKey)
                #occupancy prediction
                self.cparser.add_option('occupancy_prediction_table_name', dest='occupancyTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('predict_occupancy', dest = 'predictOccupancy', type = 'string', keys = self.ConfigFileKey)

                ## outputs
                # space temp trajectory
                self.cparser.add_option('spt_trajectory_table_name', dest='sptTrajectoryTableName', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_trajectory_table_floor_designator', dest='sptTrajectoryTableFloorDesignator', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_trajectory_sat_or_rat', dest='sat_or_rat', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('spt_trajectory_param_savepoint', dest='sptTrajectoryParamSavepoint', type='string', keys=self.ConfigFileKey)

                self.cparser.add_option('output_startup', dest='outputStartup', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('output_rampdown', dest='outputRampdown', type='string', keys=self.ConfigFileKey)
                self.cparser.add_option('output_space_temp_trajectory', dest='outputSptTrajectory', type='string', keys=self.ConfigFileKey)

                ''' added by ashwath for GP control '''
                self.cparser.add_option('steam_table_name', dest='steamTableName', type='string', keys=self.ConfigFileKey)
                ''' added by ashwath for Weather '''
                self.cparser.add_option('weather_obs_table_name', dest='weatherObsTableName', type='string',keys=self.ConfigFileKey)
                self.cparser.add_option('weather_hour_table_name', dest='weatherHourTableName', type='string',keys=self.ConfigFileKey)
                self.cparser.add_option('weather_DB', dest='weatherDB', type ='string', keys=self.ConfigFileKey)


		

        def getObject(self):
                raw_options = self.cparser.parse()
                self.floorList = self.getFloorList()
                self.floorListKeyFloor = self.getFloorListKeyFloor()
                self.equipmentNumberKeyFloor = self.getEquipmentNumberKeyFloor()
                self.quadrantKeyFloor = self.getQuadrantKeyFloor()
                self.equipmentList = list(set(raw_options.equipmentsList.strip().replace(' ', '').split(',')))
                self.quadrantList = list(set(raw_options.quadrantList.strip().replace(' ', '').split(',')))
                self.zoneList = ["'" + i + "'" for i in list(set(raw_options.zoneList.strip().replace(' ', '').split(',')))]
                self.zoneKeyFloor = self.getZoneKeyFloor()

                self.db = raw_options.db
                self.server = raw_options.server
                self.uid = raw_options.uid
                self.pwd = raw_options.pwd

                self.buildingOpenHour = datetime.time(int(raw_options.buildingOpenHour),00)
                self.buildingCloseHour = datetime.time(int(raw_options.buildingCloseHour),00)
                
                
                ''' spt prediction params '''
                self.sptPredictionParams = dummy()
                self.sptPredictionParams.tableName = raw_options.sptPredictionTableName
                self.sptPredictionParams.tableFloorDesignator = raw_options.sptPredictionTableFloorDesignator
                self.sptPredictionParams.hasQuadrants = bool(int(raw_options.sptPredictionHasQuadrants))


                ''' space temperature params'''
                self.sptParams = dummy()
                self.sptParams.tableName = raw_options.sptTableName
                self.sptParams.equalityConstraintList = raw_options.sptEqualityConstraintList.strip().replace(' ', '').split(',')
                self.sptParams.constraintValListKeyFloor = self.makeEqualityConstraintListKeyFloor(self.sptParams.equalityConstraintList)

                self.sptParams.hasQuadrants = bool(int(raw_options.sptPredictionHasQuadrants))


                ''' supply air temperature params '''
                self.satParams = dummy()
                self.satParams.tableName = raw_options.satTableName
                self.satParams.equalityConstraintList = raw_options.satEqualityConstraintList.strip().replace(' ', '').split(',')
                self.satParams.constraintValListKeyFloor = self.makeEqualityConstraintListKeyFloor(self.satParams.equalityConstraintList)

                ''' supply air temperature set point params '''
                self.satSPParams = dummy()
                self.satSPParams.tableName = raw_options.satSTableName
                self.satSPParams.equalityConstraintList = raw_options.satSEqualityConstraintList.strip().replace(' ', '').split(',')
                self.satSPParams.constraintValListKeyFloor = self.makeEqualityConstraintListKeyFloor(self.satSPParams.equalityConstraintList)

                ''' return air temperature params '''
                self.ratParams = dummy()
                self.ratParams.tableName = raw_options.ratTableName
                self.ratParams.equalityConstraintList = raw_options.ratEqualityConstraintList.strip().replace(' ', '').split(',')
                self.ratParams.constraintValListKeyFloor = self.makeEqualityConstraintListKeyFloor(self.ratParams.equalityConstraintList)
                

                ''' steam prediction params '''
                self.steamPredictionParams = dummy()
                self.steamPredictionParams.tableName = raw_options.steamPredictionTableName
                self.steamPredictionParams.hasSteamSupply = bool(int(raw_options.hasSteamSupply))


                ''' electricity prediction params '''
                self.electricityPredictionParams = dummy()
                self.electricityPredictionParams.tableName = raw_options.electricityPredictionTableName

                ''' rampdown params '''
                self.rampdownParams = dummy()
                self.rampdownParams.tableName = raw_options.rampDownTableName
                self.rampdownParams.outputRampdown = raw_options.outputRampdown

                ''' startup params '''
                self.startupParams = dummy()

                self.startupParams.tableName = raw_options.startupTableName
                self.startupParams.equalityConstraintList = raw_options.startupEqualityConstraintList.strip().replace(' ', '').split(',')
                self.startupParams.outputStartup = raw_options.outputStartup

                ''' space temperature trajectory params '''
                self.sptTrajectoryParams = dummy()
                self.sptTrajectoryParams.tableName = raw_options.sptTrajectoryTableName
                self.sptTrajectoryParams.tableFloorDesignator = raw_options.sptTrajectoryTableFloorDesignator
                self.sptTrajectoryParams.sat_or_rat = raw_options.sat_or_rat.lower().strip().replace(' ', '').split(',')
                self.sptTrajectoryParams.outputSptTrajectory = raw_options.outputSptTrajectory
                self.sptTrajectoryParams.paramSavepoint = raw_options.sptTrajectoryParamSavepoint
                self.sptTrajectoryParams.hasQuadrants = bool(int(raw_options.sptPredictionHasQuadrants))

                ''' steam params '''
                self.steamParams = dummy()
                self.steamParams.tableName = raw_options.steamTableName

                ''' weather observation history params '''
                self.weatherObsParams = dummy()
                self.weatherObsParams.tableName = raw_options.weatherObsTableName

                ''' weather hourly forecast params'''
                self.weatherHourParams = dummy()
                self.weatherHourParams.tableName = raw_options.weatherHourTableName

                ''' occupancy params '''
                self.occupancyParams = dummy()
                self.occupancyParams.tableName = raw_options.occupancyTableName
                self.occupancyParams.predictOccupancy = bool(int(raw_options.predictOccupancy))



        def makeEqualityConstraintListKeyFloor(self, equalityConstraintList):
                equalityConstraintListKeyFloor = {}
                for floor in self.floorList:
                        if floor not in equalityConstraintListKeyFloor:
                                equalityConstraintListKeyFloor[floor] = []
                        for element in equalityConstraintList:
                                if element.lower() == "floor":
                                        equalityConstraintListKeyFloor[floor].append(self.floorListKeyFloor[floor][0])
                                if element.lower() == "equipment_no":
                                        equalityConstraintListKeyFloor[floor].append(self.equipmentNumberKeyFloor[floor][0])
                                if element.lower() == "quadrant":
                                        equalityConstraintListKeyFloor[floor].append(self.quadrantKeyFloor[floor][0])
                                if element.lower() == "zone":
                                        equalityConstraintListKeyFloor[floor].append(self.zoneKeyFloor[floor][0])
                return equalityConstraintListKeyFloor
        
        def getFloorList(self):
                finalFloorList = []
                options = self.cparser.parse()
                floorListString = options.floorList
                if floorListString == '':
                        return
                flist = floorListString.strip().replace(' ', '').split(',')
                if flist[0] == 'range':
                        flist = range(flist[1], flist[2]+1)
                for floor in flist:
                        if len(list(floor)) == 1:
                                finalFloorList.append("'F0"+floor+"'")
                        else:
                                finalFloorList.append("'F"+floor+"'")
                return finalFloorList
                
        def getFloorListKeyFloor(self):
                rdict = {}
                floorList = self.floorList
                for i in floorList:
                        rdict[i] = [i]
                return rdict

        def getZoneKeyFloor(self):
                rdict= {}
                floorList = self.floorList
                options = self.cparser.parse()
                zoneListString = options.zoneList
                if zoneListString == '':
                        return
                zoneList = zoneListString.strip().replace(' ', '').split(',')
                for i in range(len(zoneList)):
                        if i >= len(floorList):
                                break
                        rdict[floorList[i]] = ["'"+zoneList[i]+"'"]
                return rdict

        def getEquipmentNumberKeyFloor(self):
                rdict = {}
                options = self.cparser.parse()
                equipListString = options.equipmentsList
                if equipListString == '':
                        return
                eqList = equipListString.strip().replace(' ', '').split(',')
                floorList = self.floorList
                for i in range(len(eqList)):
                        if i >= len(floorList):
                                break
                        rdict[floorList[i]] = ["'"+eqList[i]+"'"]
                return rdict

        def getQuadrantKeyFloor(self):
                rdict = {}
                options = self.cparser.parse()
                quadListString = options.quadrantList
                if quadListString == '':
                        return
                qList = quadListString.strip().replace(' ', '').split(',')
                floorList = self.floorList
                for i in range(len(qList)):
                        if i >= len(floorList):
                                break
                        rdict[floorList[i]] = ["'"+qList[i]+"'"]
                return rdict
                

	
