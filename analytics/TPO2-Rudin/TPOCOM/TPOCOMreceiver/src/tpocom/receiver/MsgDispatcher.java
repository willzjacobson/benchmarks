package tpocom.receiver;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.Value;

public class MsgDispatcher {

	public MsgDispatcher(ConnectionManager conMan, Map<String, InterestPoint> pointsMap) {
		this.conMan = conMan;
		this.pointsMap = pointsMap;
		this.constructPtIdStrMap();
	}

	public void despatch(List<Point> points) throws ClassNotFoundException,
			SQLException {
		for (Point pt : points) {
			boolean matchFound = false;
			for (Pattern pat : this.idPatternToPtNameMap.keySet()) {
				if (pat.matcher(getPtIdStr(pt)).find()) {
					writePointToStore(pt, this.idPatternToPtNameMap.get(pat));
					matchFound = true;
					System.out.println("+++++++ Match found - " + getPtIdStr(pt));
				}
			}
			if(!matchFound){
				System.out.println("------- No match - " + getPtIdStr(pt));
			}
		}
	}
	
	private void writePointToStore(Point pt, String pointName) throws ClassNotFoundException, SQLException{
		InterestPoint inPoint = this.pointsMap.get(pointName);
		Connection conn = this.conMan.getConnection(inPoint.getDbConnectionName());
		String tableName = this.conMan.getTableName(inPoint.getDbConnectionName());
		StringBuffer colNameStr = new StringBuffer();
		StringBuffer colValStr = new StringBuffer();
		//build comma delimited variable and value list
		String delim = "";
		for(String ptAttr:inPoint.getPtColMap().keySet()){
			String colName = inPoint.getPtColMap().get(ptAttr);
			colNameStr.append(delim).append(colName);
			colValStr.append(delim).append('?');
			delim = ",";
		}
		
		// put them all together. 
		StringBuffer sqlQuery = new StringBuffer();
		sqlQuery.append("insert into "+tableName+"(");
		sqlQuery.append(colNameStr);
		sqlQuery.append(") values(");
		sqlQuery.append(colValStr);
		sqlQuery.append(')');
		
				
		PreparedStatement stmt = conn.prepareStatement(sqlQuery.toString());
		Map<String, String> ptColMap = inPoint.getPtColMap(); 
		int parNo = 1;
		for(String ptAttr:ptColMap.keySet()){
			setValue(stmt, pt, ptAttr, parNo);
			parNo+=1;
		}
		stmt.executeUpdate();
		stmt.close();
	}
	
	
	private void setValue(PreparedStatement stmt, Point pt, String ptAttr, int parNo) throws SQLException{
		if (ptAttr.equals("Pbs_Loc_A1")){
			stmt.setString(parNo, pt.getPbs_Loc_A1());
		} else if (ptAttr.equals("Pbs_Loc_A2")){
			stmt.setString(parNo, pt.getPbs_Loc_A2());
		} else if (ptAttr.equals("Pbs_Loc_A3")){
			stmt.setString(parNo, pt.getPbs_Loc_A3());
		} else if (ptAttr.equals("Pbs_Loc_A4")){
			stmt.setString(parNo, pt.getPbs_Loc_A4());
		} else if (ptAttr.equals("Pbs_Sys_T")){
			stmt.setString(parNo, pt.getPbs_Sys_S());
		} else if (ptAttr.equals("Pbs_Sys_S")){
			stmt.setString(parNo, pt.getPbs_Sys_T());
		} else if (ptAttr.equals("Pbs_Eq_L1")){
			stmt.setString(parNo, pt.getPbs_Eq_L1());
		} else if (ptAttr.equals("Pbs_Eq_L2")){
			stmt.setString(parNo, pt.getPbs_Eq_L2());
		} else if (ptAttr.equals("Pbs_Eq_L3")){
			stmt.setString(parNo, pt.getPbs_Eq_L3());
		} else if (ptAttr.equals("Pbs_Eq_n")){
			stmt.setString(parNo, pt.getPbs_Eq_n());
		} else if (ptAttr.equals("Sign_Code")){
			stmt.setString(parNo, pt.getSign_Code());
		} else if (ptAttr.equals("Point_Type")){
			stmt.setString(parNo, pt.getPoint_Type());
		} else if (ptAttr.equals("ts")){
			if ((pt.getPbs_Sys_S().equals("SEC"))&&(pt.getPbs_Eq_L1().equals("CNT"))&&(pt.getPbs_Eq_L2().equals("PEO"))&&(pt.getPbs_Eq_L3().equals("BUI"))){
			   stmt.setTimestamp(parNo, new Timestamp(pt.getTs().getTime()));
			}
			else{
			   Date ts = pt.getTs();
			   GregorianCalendar gregCal = new GregorianCalendar();		
			   gregCal.setTime(ts);		
			   gregCal.set(Calendar.SECOND, 0);
			   gregCal.set(Calendar.MILLISECOND, 0);		
			   int nowMinute = gregCal.get(Calendar.MINUTE);		
			   int roundMinute = 15 * (nowMinute / 15);				
			   gregCal.set(Calendar.MINUTE, roundMinute);		
			   ts = gregCal.getTime();
   			   stmt.setTimestamp(parNo, new Timestamp(ts.getTime()));
			   System.out.println("Timestamp set to ts");
			}
		} else if (ptAttr.equals("refTs")){
			stmt.setTimestamp(parNo, new Timestamp(pt.getRefTs().getTime()));
			System.out.println("Timestamp set to refTs");
		} else if (ptAttr.equals("Value")) {
			List<Value> vals = pt.getValues();
			//TODO : how to handle multiple values
			Value val = vals.get(0);
			if (val.isBoolean()){
				stmt.setBoolean(parNo, val.getValue_Bool());
			}else if (val.isNumber()){
				stmt.setDouble(parNo, val.getValue_No());
			}else if (val.isText()) {
				stmt.setString(parNo, val.getValue_Tx());
			}
		}

	}
	
	private String getPtIdStr(Point pt){
		StringBuffer str = new StringBuffer();
		str.append(pt.getPbs_Loc_A1());
		str.append(pt.getPbs_Loc_A2());
		str.append(pt.getPbs_Loc_A3());
		str.append(pt.getPbs_Loc_A4());
		str.append(pt.getPbs_Sys_T());
		str.append(pt.getPbs_Sys_S());
		str.append(pt.getPbs_Eq_L1());
		str.append(pt.getPbs_Eq_L2());
		str.append(pt.getPbs_Eq_L3());
		str.append(pt.getPbs_Eq_n());
		str.append(pt.getSign_Code());
		str.append(pt.getSign_Prog());
		str.append(pt.getPoint_Type());
		return str.toString();
	}
	
	private void constructPtIdStrMap() {
		this.idPatternToPtNameMap = new HashMap<Pattern, String>();
		List<String> threeLetterIds = Arrays.asList("Pbs_Loc_A1", "Pbs_Loc_A2",
				"Pbs_Loc_A3", "Pbs_Loc_A4", "Pbs_Sys_T", "Pbs_Sys_S",
				"Pbs_Eq_L1", "Pbs_Eq_L2", "Pbs_Eq_L3", "Pbs_Eq_n");
		List<String> varLetterIds = Arrays.asList("Sign_Code","Sign_Prog","Point_Type");
		
		for (String ptName : this.pointsMap.keySet()) {
			InterestPoint ip = this.pointsMap.get(ptName);
			Map<String, String>ptColMap = ip.getPtIdentifiersMap();
			StringBuffer str = new StringBuffer();

			// construct regular expressions for three letter identifiers in
			// case they are not in the config 
			for (String id : threeLetterIds) {
				if (ptColMap.containsKey(id)) {
					str.append(ptColMap.get(id));
				} else {
					str.append("...");
				}
			}
			
			// just stack the variable letter identifiers at the end in the
			// order from the list above
			for (String id: varLetterIds){
				if (ptColMap.containsKey(id)) {
					str.append(ptColMap.get(id));
				}				
			}
			this.idPatternToPtNameMap.put(Pattern.compile(str.toString()), ptName);
		}
	}
		
	private ConnectionManager conMan;
	private Map<String, InterestPoint> pointsMap;
	private Map<Pattern, String> idPatternToPtNameMap;
}
