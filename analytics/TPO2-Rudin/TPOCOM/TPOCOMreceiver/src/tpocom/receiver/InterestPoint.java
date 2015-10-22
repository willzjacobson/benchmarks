package tpocom.receiver;

import java.util.Map;

/**
 * Interest Point has the details to identify a given point and to 
 * store the given point in the specified database
 * @author vivek
 *
 */
public class InterestPoint {

	public InterestPoint(String dbconName, Map<String, String> ptIdentifiersMap,
			Map<String, String> ptColMap) {
		this.dbConnectionName = dbconName;
		this.ptIdentifiersMap = ptIdentifiersMap;
		this.ptColMap = ptColMap;
	}
	
	/**
	 * Returns the database name where this InterestPoint is to be stored
	 * @return
	 */
	public String getDbConnectionName() {
		return dbConnectionName;
	}
	
	/**
	 * Returns a map of the Point Identifiers.
	 * @return
	 */
	public Map<String, String> getPtIdentifiersMap() {
		return ptIdentifiersMap;
	}

	/**
	 * Returns a mapping between the point values and the database columns
	 * @return
	 */
	public Map<String, String> getPtColMap() {
		return ptColMap;
	}

	private String dbConnectionName;
	private Map<String, String> ptIdentifiersMap;
	private Map<String, String> ptColMap;
}
