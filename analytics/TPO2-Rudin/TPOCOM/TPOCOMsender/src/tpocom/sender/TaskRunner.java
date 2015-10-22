package tpocom.sender;

import java.io.IOException;
import java.rmi.RemoteException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import communicator.TPOCOMcommunicator;

import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.XmlToolException;
import tpo.adapter.client.impl.Wssb2Client.MsgType;

/**
 * This class handle the job of polling the TPO databases to send the Points for
 * all the specified PointConfig to the SIF server.
 * @author vivek
 *
 */
public class TaskRunner implements Runnable {

	public TaskRunner(ConnectionManager conMan,
			Map<String, PointConfig> pointConfigs,
			RowPointConverter rpConverter,
			TPOCOMcommunicator tpocom) throws RemoteException, XmlToolException {
		this.conMan = conMan;
		this.pointConfigs = pointConfigs;
		this.rpConverter = rpConverter;
		this.tpocom = tpocom;
	}

	@Override
	public void run() {
		System.out.println("------------Task------------");
		// TODO Auto-generated method stub
		for(String pointConfigName: this.pointConfigs.keySet()){
			try {
				String lastSentID = this.fetchLastSentID(pointConfigName);
				int newRows = fetchNumberOfNewRows(pointConfigName, lastSentID);
				System.out.print(pointConfigName+" - "+newRows+ " new rows available ");
				if(newRows > 0) {
					String latestAvailableID = fetchLatestAvailableID(pointConfigName);
					ResultSet rs = fetchResultSet(pointConfigName, lastSentID, latestAvailableID);
					
					List<Point> pointList = this.getPointList(
							this.pointConfigs.get(pointConfigName), rs);	
					rs.close();
					List<Point> measurePoints = new ArrayList<Point>();
					List<Point> statusPoints = new ArrayList<Point>();
					List<Point> alarmPoints = new ArrayList<Point>();
					
					// group the points based on their type
					for(Point pt: pointList){
						if(pt.getPoint_Type().equalsIgnoreCase(MsgType.MEASURE.toString())){
							measurePoints.add(pt);
						} else if (pt.getPoint_Type().equalsIgnoreCase(MsgType.STATUS.toString())){
							statusPoints.add(pt);
						} else if (pt.getPoint_Type().equalsIgnoreCase(MsgType.ALARM.toString())){
							alarmPoints.add(pt);
						}
					}
					
					/**
					 * Send points by batching them into groups of 100. Also
					 * sleep between successive web service calls and not
					 * overwhelm SIF with requests
					 */
					int partitionSize = 100; 
					for (int i = 0; i < measurePoints.size(); i += partitionSize) {
						this.tpocom.sendPoints(measurePoints.subList(i,
					            i + Math.min(partitionSize, measurePoints.size() - i)), 
					            MsgType.MEASURE);
						Thread.sleep(1000); // sleep for a second.
					}
					for (int i = 0; i < statusPoints.size(); i += partitionSize) {
						this.tpocom.sendPoints(statusPoints.subList(i,
					            i + Math.min(partitionSize, statusPoints.size() - i)),
					            MsgType.STATUS);
						Thread.sleep(1000); // sleep for a second.
					}
					for (int i = 0; i < alarmPoints.size(); i += partitionSize) {
						this.tpocom.sendPoints(alarmPoints.subList(i,
					            i + Math.min(partitionSize, alarmPoints.size() - i)),
					            MsgType.ALARM);
						Thread.sleep(1000); // sleep for a second.
					}
					
					// update the timestamp only if the send succeeds\
					updateLastSentID(latestAvailableID, pointConfigName);					
					System.out.println("- " + pointList.size()+" points sent");
				} else {
					System.out.println("- 0 points sent");
				}
			} catch (RemoteException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (XmlToolException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (Exception e){
				e.printStackTrace();
			}
		}
		System.out.println("----------------------------");
	}

	private String fetchLastSentID(String pointConfigName) throws IOException, ClassNotFoundException, SQLException {
		PointConfig ptConfig = this.pointConfigs.get(pointConfigName);
		Connection conn = this.conMan.getConnection(ptConfig.getTrackerDBConName());
		String tableName = this.conMan.getTableName(ptConfig.getTrackerDBConName());
		String sqlQuery = "SELECT MAX("+ptConfig.getTrackerColName()+") from "+tableName;
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sqlQuery);
		rs.next();
		String retString = rs.getString(1);
		rs.close();
		return retString;
	}
	
	private void updateLastSentID(String latestSendID, String pointConfigName) throws ClassNotFoundException, SQLException{
		PointConfig ptConfig = this.pointConfigs.get(pointConfigName);
		Connection conn = this.conMan.getConnection(ptConfig.getTrackerDBConName());
		String tableName = this.conMan.getTableName(ptConfig.getTrackerDBConName());
		String sqlQuery = "insert into "+tableName+"("+ptConfig.getTrackerColName()+") values('"+latestSendID+"')";
		Statement stmt = conn.createStatement();
		stmt.executeUpdate(sqlQuery);
		stmt.close();
	}
	
	private String fetchLatestAvailableID(String pointConfigName) throws ClassNotFoundException, SQLException, IOException {
		String lastSentID = this.fetchLastSentID(pointConfigName);
		PointConfig ptConfig = this.pointConfigs.get(pointConfigName);
		String tableName = this.conMan.getTableName(ptConfig.getDbConnectionName());
		Connection conn = this.conMan.getConnection(ptConfig.getDbConnectionName());
		String sqlQuery = "SELECT MAX("
				+ ptConfig.getIdentifierColName() + ") from " + tableName + " where "
				+ ptConfig.getIdentifierColName()+ " > '" + lastSentID + "'";
		PreparedStatement query = conn.prepareStatement(sqlQuery);
		ResultSet rs = query.executeQuery();
		rs.next();	
		String maxID = rs.getString(1);
	
		rs.close();
		return maxID;
	}
	
	private int fetchNumberOfNewRows(String pointConfigName, String lastSentID) throws SQLException, IOException, ClassNotFoundException{
		PointConfig ptConfig = this.pointConfigs.get(pointConfigName);
		String tableName = this.conMan.getTableName(ptConfig.getDbConnectionName());
		Connection conn = this.conMan.getConnection(ptConfig.getDbConnectionName());
		String sqlquery = "SELECT COUNT(*) as CNT from " + tableName
				+ " where " + ptConfig.getIdentifierColName() + " > '"
				+ lastSentID + "'";
		PreparedStatement query = conn.prepareStatement(sqlquery);
		ResultSet rs = query.executeQuery();
		rs.next();
		int newRows = rs.getInt("CNT");
		rs.close();
		
		return newRows;
	}

	private ResultSet fetchResultSet(String pointConfigName, String lastSentID, String latestAvailableID) throws IOException, ClassNotFoundException, SQLException {
		PointConfig ptConfig = this.pointConfigs.get(pointConfigName);
		String tableName = this.conMan.getTableName(ptConfig.getDbConnectionName());
		String sqlQuery = "SELECT * from " + tableName + " where "
				+ ptConfig.getIdentifierColName() + " > '" + lastSentID + "' AND "
				+ ptConfig.getIdentifierColName() + " <= '" + latestAvailableID
				+ "' ORDER BY " + ptConfig.getIdentifierColName();
		Connection conn = this.conMan.getConnection(ptConfig.getDbConnectionName());
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sqlQuery);
		return rs;
	}
	
	private List<Point> getPointList(PointConfig ptConfig, ResultSet rs) throws SQLException{
		return this.rpConverter.getPointsFromRows(ptConfig, rs);
	}

	private ConnectionManager conMan;
	private Map<String, PointConfig> pointConfigs;
	private RowPointConverter rpConverter;
	private TPOCOMcommunicator tpocom;
}
