package tpocom.sender;


import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicLong;

import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.Value;
/**
 * This class provides the functionality of converting the rows in a result set to the 
 * given Point type using the details in the point Config.
 * @author vivek
 *
 */
public class RowPointConverter {

	public RowPointConverter() {
		// TODO Auto-generated constructor stub
	}
	
	/**
	 * This method takes in a ResultSet and a PointConfig and gives out list of
	 * Point constructed using the details in the point Config.
	 * 
	 * @param ptConfig
	 * @param rs
	 * @return
	 * @throws SQLException
	 */
	public List<Point> getPointsFromRows(PointConfig ptConfig, ResultSet rs) throws SQLException{
		Map<String, String>constants = ptConfig.getConstants();
		Map<String, ValueVarConfig>valueCodes = ptConfig.getValueCodeMap();
		Map<String,PointVarConfig> variables =  ptConfig.getPtVarConfigMap();
		
		//Selex has this weird design that a measure can have upto 100 Values in it while
		//a status can have only one value in it.
		int partitionSize = 1;
		if(constants.get("Point_Type").equals("measure")){
			partitionSize = 50;
		}
		
		//map to collect Values that belong to each of Point types for the given Point Config. 
		Map<List<DataObject>, List<Value>> store = new HashMap<List<DataObject>, List<Value>>();
		
		while(rs.next()){
			List<DataObject> pointVariables  = new ArrayList<DataObject>();
			//get all the variables common to all Value Objects for this point
			for (String colName : variables.keySet()) {
				String pointVarType = variables.get(colName).getPointVarType();
				DataObject dobject = new DataObject(rs, colName, pointVarType);
				pointVariables.add(dobject);
			}
			
			//If we have no value codes, just add a empty ArrayList<Value> with the point variables key
			//Alarm messages have no Value objects.
			if (valueCodes.isEmpty()) {
				store.put(pointVariables, new ArrayList<Value>());
			}
			//If we have Value codes, add the value code as additional key with the point variables and
			// then group the values with same keys.			
			for (String colName : valueCodes.keySet()) {
				ValueVarConfig valVarConfig = valueCodes.get(colName);
				List<DataObject> specificPointVariables = new ArrayList<DataObject>(
						pointVariables);
				DataObject dobj = new DataObject();
				dobj.setText(valVarConfig.getValueCode());
				specificPointVariables.add(dobj);
				Value val = getValueObj(rs, colName,
						valVarConfig.getOutputDataType(),
						ptConfig.getValueAttrConfig());
				if (!store.containsKey(specificPointVariables)) {
					store.put(specificPointVariables, new ArrayList<Value>());
				}
				store.get(specificPointVariables).add(val);
			}
			
		} 
		
		List<Point> pointlist = new ArrayList<Point>();
		//now create a batch of points to be sent
		for(List<DataObject> keys: store.keySet()){
			List<Value> values = store.get(keys);
			
			//partition the values into groups
			
			List<List<Value>> valueBatches = new ArrayList<List<Value>>();
			for (int i = 0; i < values.size(); i += partitionSize) {
				valueBatches.add(values.subList(i,
			            i + Math.min(partitionSize, values.size() - i)));
			}
			
			// For Points that have not cbeen configured to send and values, 
			// the configuration should carry sign code in the constants. 
			// Alarms work this way.
			if (valueBatches.isEmpty()){
				Point pt = new Point();
				initializePoint(pt);
				//set all the constants in the point config 
				for (String ptAttr: constants.keySet()){
					callStringMethodsOnPoint(pt, ptAttr, constants.get(ptAttr));
				}
				//set all variables in the list of DataObject keys
				String [] varkeys = variables.keySet().toArray(new String[0]);
				for (int i =0 ; i < variables.size(); i++){
					callMethodsOnPoint(pt, variables.get(varkeys[i]).getPointAttrName(), keys.get(i));
				}
				//generate unique timestamp and set it
				DataObject timestamp = new DataObject();
				timestamp.setDate(uniqueCurrentTimeMS());
				callMethodsOnPoint(pt, "Ts", timestamp);				
				pt.setBad(false);
				//set pbs code
				setPbs(pt);	
				pointlist.add(pt);					
			}
			
			//create one Point for each batch of values
			for(List<Value> oneBatchVals:valueBatches){
				Point pt = new Point();
				initializePoint(pt);
				
				//set all the constants in the point config 
				for (String ptAttr: constants.keySet()){
					callStringMethodsOnPoint(pt, ptAttr, constants.get(ptAttr));
				}
				
				//set all variables in the list of DataObject keys
				String [] varkeys = variables.keySet().toArray(new String[0]);
				for (int i =0 ; i < variables.size(); i++){
					callMethodsOnPoint(pt, variables.get(varkeys[i]).getPointAttrName(), keys.get(i));
				}
				//set the value code
				callMethodsOnPoint(pt, "Sign_Code", keys.get(keys.size()-1));
				
				//generate unique timestamp and set it
				DataObject timestamp = new DataObject();
				timestamp.setDate(uniqueCurrentTimeMS());
				callMethodsOnPoint(pt, "Ts", timestamp);
				
				pt.setBad(false);
				
				//set pbs code
				setPbs(pt);
			
				pt.setValues(oneBatchVals);
				if(oneBatchVals.size()> 1){
					pt.setSamp(new Long(2000));
				}
					
				pointlist.add(pt);			
			}
		}
		return pointlist;
	}
	
	private Value getValueObj(ResultSet rs, String colName, String type,
			Map<String,ValueAttrConfig> valueAttrConFig) throws SQLException {
		Value value = new Value();
		
		if(type.equals("string")){
			value.setValue_Tx(rs.getString(colName));
		} else if(type.equals("double")){
			value.setValue_No(rs.getDouble(colName));
		} else if(type.equals("boolean")){
			value.setValue_Bool(rs.getBoolean(colName));
		}
		
		// EXPAND THIS and structure better in case they add more attributes to value
		for (String attrColName: valueAttrConFig.keySet()){
			ValueAttrConfig config = valueAttrConFig.get(attrColName);
			if(config.getValueDataType().equals("date")){
				if(config.getValueAttrName().equals("RefTs")){
					value.setRefTs(rs.getTimestamp(attrColName));
				}
			}
		}	
		return value;
	}
	
	private void callMethodsOnPoint(Point pt, String methodname, DataObject dataObject) {
		// dataObject after loading from result set is empty,
		//then the value is not to be passed.
		if (dataObject.isEmpty()){
			return;
		}		
		final String[] stringmethods = { "Pbs_Loc_A1", "Pbs_Loc_A2",
				"Pbs_Loc_A3", "Pbs_Loc_A4", "Pbs_Eq_L1", "Pbs_Eq_L2",
				"Pbs_Eq_L3", "Pbs_Sys_T", "Pbs_Sys_S", "Sign_Prog", "Sender",
				"Sign_Code", "Point_Type", "Pbs_Native", "Realtime", "Pbs_Eq_n", "Lob_Pbs", "Lob_Sign"};
		Set<String> stringmethodsset = new HashSet<String>(Arrays.asList(stringmethods));
		
		if (stringmethodsset.contains(methodname)){
			callStringMethodsOnPoint(pt, methodname, dataObject.getText());
		} else if(methodname.equals("RefTs")){
			pt.setRefTs(dataObject.getDate());
		} else if(methodname.equals("Ts")){
			pt.setTs(dataObject.getDate());
		} else if(methodname.equals("Alarm_Init_Ts")){
			pt.setAlarm_Init_Ts(dataObject.getDate());
		} else if(methodname.equals("Alarm_State")){
			pt.setAlarm_State(dataObject.getInteger());
		} else if(methodname.equals("Alarm_Prio")){
			pt.setAlarm_Prio(dataObject.getInteger());
		} else if(methodname.equals("Alarm_Norm_Ts")){
			pt.setAlarm_Norm_Ts(dataObject.getDate());
		}
	}

	private static final AtomicLong LAST_TIME_MS = new AtomicLong();
	private static Date uniqueCurrentTimeMS() {
	    long now = System.currentTimeMillis();
	    while(true) {
	        long lastTime = LAST_TIME_MS.get();
	        if (lastTime >= now)
	            now = lastTime+1;
	        if (LAST_TIME_MS.compareAndSet(lastTime, now)){
	        	Calendar cal = Calendar.getInstance();
	        	cal.setTimeInMillis(now);
	        	return cal.getTime();
	        }
	    }
	}
	
	private void setPbs(Point pt) {
		StringBuffer pbsString = new StringBuffer();
		pbsString.append(pt.getPbs_Loc_A1());
		pbsString.append(pt.getPbs_Loc_A2());
		pbsString.append(pt.getPbs_Loc_A3());
		pbsString.append(pt.getPbs_Loc_A4());
		pbsString.append(pt.getPbs_Sys_T());
		pbsString.append(pt.getPbs_Sys_S());
		pbsString.append(pt.getPbs_Eq_L1());
		pbsString.append(pt.getPbs_Eq_L2());
		pbsString.append(pt.getPbs_Eq_L3());
		pbsString.append(pt.getPbs_Eq_n());
		pt.setPbs(pbsString.toString());
	}
	
	private void initializePoint(Point point) {
		String def3codeString = "---";
		String defEmptyString = "";
		point.setPbs_Loc_A1(def3codeString);
		point.setPbs_Loc_A2(def3codeString);
		point.setPbs_Loc_A3(def3codeString);
		point.setPbs_Loc_A4(def3codeString);
		point.setPbs_Sys_T(def3codeString);
		point.setPbs_Sys_S(def3codeString);
		point.setPbs_Eq_L1(def3codeString);
		point.setPbs_Eq_L2(def3codeString);
		point.setPbs_Eq_L3(def3codeString);
		point.setPbs_Eq_n(def3codeString);
		point.setSign_Prog(defEmptyString);
		point.setSign_Code(defEmptyString);
		point.setSender(defEmptyString);
		point.setPoint_Type(defEmptyString);
		point.setPbs_Native(defEmptyString);
		point.setRealtime(defEmptyString);
	}

	private void callStringMethodsOnPoint(Point point, String methodName, String param){
		if(methodName.equals("Pbs_Loc_A1")){
			point.setPbs_Loc_A1(param);
		} else if(methodName.equals("Pbs_Loc_A2")){
			//temporary hack for 345 park
			if(!param.equals("---") && param.length()<3){
				int zoneNo = Integer.parseInt(param);
				param = String.format("Z%02d", zoneNo);
			}
			point.setPbs_Loc_A2(param);
		} else if(methodName.equals("Pbs_Loc_A3")) {
			//temporary hack for 345 park
			if(!param.equals("---") && param.length()<3){
				int floorNo = Integer.parseInt(param);
				param = String.format("F%02d", floorNo);
			}			
			point.setPbs_Loc_A3(param);
		} else if(methodName.equals("Pbs_Loc_A4")){
			//temporary hack for 345 park
			if(!param.equals("---") && param.length()<3){
				param = String.format("C%s", param);
			}						
			point.setPbs_Loc_A4(param);
		} else if(methodName.equals("Pbs_Eq_L1")){
			point.setPbs_Eq_L1(param);
		} else if(methodName.equals("Pbs_Eq_L2")){
			point.setPbs_Eq_L2(param);
		} else if(methodName.equals("Pbs_Eq_L3")){
			point.setPbs_Eq_L3(param);
		} else if(methodName.equals("Pbs_Sys_T")){
			point.setPbs_Sys_T(param);
		} else if(methodName.equals("Pbs_Sys_S")){
			point.setPbs_Sys_S(param);
		} else if(methodName.equals("Sign_Prog")){
			point.setSign_Prog(param);
		} else if(methodName.equals("Sender")){
			point.setSender(param);
		} else if(methodName.equals("Sign_Code")) {
			point.setSign_Code(param);
		} else if(methodName.equals("Point_Type")) {
			point.setPoint_Type(param);
		} else if(methodName.equals("Pbs_Native")) {
			point.setPbs_Native(param);
		} else if(methodName.equals("Realtime")) {
			point.setRealtime(param);
		} else if(methodName.equals("Pbs_Eq_n")){
			point.setPbs_Eq_n(param);
		} else if (methodName.equals("Lob_Pbs")){
			point.setLob_Pbs(param);
		} else if (methodName.equals("Lob_Sign")) {
			point.setLob_Sign(param);
		}
	}
}