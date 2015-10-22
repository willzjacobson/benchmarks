package tpocom.sender;

/**
 * DbDetail class stores all the information required to make connectino to 
 * a particular database. It also stores the table name to be used for this
 * DbDetail.
 * @author vivek
 *
 */
public class DbDetail {
	
	/**
	 * Takes in host, port, database, table, username and password for the db
	 * @param host
	 * @param port
	 * @param database
	 * @param table
	 * @param user
	 * @param passwd
	 */
	public DbDetail(String host, String port, String database, String table,
			String user, String passwd) {
		this.host = host;
		this.database = database;
		this.port = port;
		this.table = table;
		this.user = user;
		this.password = passwd;
	}
	
	/**
	 * Returns the host name for database
	 * @return
	 */
	public String getHost() {
		return host;
	}

	/**
	 * Returns the port number for the database
	 * @return
	 */
	public String getPort() {
		return port;
	}

	/**
	 * Returns the database name
	 * @return
	 */
	public String getDatabase() {
		return database;
	}

	/**
	 * Returns the table to be used in the DbDetail
	 * @return
	 */
	public String getTable() {
		return table;
	}

	/**
	 * Returns the username
	 * @return
	 */
	public String getUser() {
		return user;
	}

	/**
	 * Returns the password
	 * @return
	 */
	public String getPassword() {
		return password;
	}

	private String host;
	private String port;
	private String database;
	private String table;
	private String user;
	private String password;
}
