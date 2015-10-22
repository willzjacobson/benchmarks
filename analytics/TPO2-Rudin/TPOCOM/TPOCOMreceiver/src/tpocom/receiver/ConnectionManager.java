package tpocom.receiver;

import java.io.IOException;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;

/**
 * This class manages all the database connections. 
 * @author vivek
 *
 */
public class ConnectionManager {

	/**
	 * Takes in a map of database names and their details required for
	 * makeing Connection Objects
	 * @param dbPropMap
	 * @throws IOException
	 */	
	public ConnectionManager(Map<String, DbDetail> dbPropMap){
		this.dbPropMap = dbPropMap;
		this.connections = new HashMap<String, Connection>();
	}

	/**
	 * Returns a Connection object for a given database dbConName.
	 * @param dbConName
	 * @return
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 */	
	public Connection getConnection(String dbConName)
			throws ClassNotFoundException, SQLException {
		if (!this.connections.containsKey(dbConName)) {
			this.makeConnection(dbConName);
		}
		//check if the connection is valid with a timeout
		// if not recreate the connection
		if(!isValid(this.connections.get(dbConName))){
			this.connections.remove(dbConName);
			this.makeConnection(dbConName);
		}
		return this.connections.get(dbConName);
	}
	
	/**
	 *Checks if this Connection is valid 
	 * @param conn
	 * @return
	 */
	private boolean isValid(Connection conn) {
		Statement stmt;
		
		try {
			stmt = conn.createStatement();
		} catch (SQLException e) {
			return false;
		}
		try {
			ResultSet rs = stmt.executeQuery("SELECT 1");
			rs.next();
			boolean ret = (rs.getObject(1)!=null);
			rs.close();
			stmt.close();
			return ret;
		} catch (SQLException e) {
			return false;
		}
	}

	/**
	 * Returns the table name for the give database details
	 * @param dbConName - name for the database details
	 * @return Table Name specified in the database details
	 */	
	public String getTableName(String dbConName) {
		return this.dbPropMap.get(dbConName).getTable();
	}

	/**
	 * Closes all the connections maintained by the connection Manager
	 * @throws SQLException
	 */	
	public void close() throws SQLException {
		for (Connection conn : this.connections.values()) {
			conn.close();
		}
	}

	/**
	 * Makes a Connection to the database dbConName and store the connection
	 * database in a map
	 * 
	 * @param dbConName - database name
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 */	
	private void makeConnection(String dbConName)
			throws ClassNotFoundException, SQLException {
		DbDetail dbprop = this.dbPropMap.get(dbConName);
		String connectString = "jdbc:jtds:sqlserver://" + dbprop.getHost()
				+ ":" + dbprop.getPort() + "/" + dbprop.getDatabase();
		Class.forName("net.sourceforge.jtds.jdbc.Driver");
		Connection conn = DriverManager.getConnection(connectString,
				dbprop.getUser(), dbprop.getPassword());
		this.connections.put(dbConName, conn);
	}

	private HashMap<String, Connection> connections;
	private Map<String, DbDetail> dbPropMap;
};
