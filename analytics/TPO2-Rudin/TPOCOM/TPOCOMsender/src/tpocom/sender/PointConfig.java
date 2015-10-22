package tpocom.sender;

import java.util.Map;

/**
 * Point class holds all the details required to construct a Point
 * object from the TPO database table
 * @author vivek
 *
 */
public class PointConfig {
	/**
	 * Takes in all the parameters that are required to describe 
	 * how to construct the Point of this type 
	 * @param dbconName
	 * @param trackerDBConName
	 * @param constants
	 * @param valueCodes
	 * @param variableTypes
	 * @param primaryCol
	 * @param trackerCol
	 * @param valueAttrMap
	 */
	public PointConfig(String dbconName, String trackerDBConName, Map<String, String> constants,
			Map<String, ValueVarConfig> valueCodes,
			Map<String, PointVarConfig> variableTypes,
			String primaryCol,
			String trackerCol,
			Map<String, ValueAttrConfig> valueAttrMap ) {
		this.dbConnectionName = dbconName;
		this.trackerDBConName = trackerDBConName;
		this.constants = constants;
		this.valueCodes = valueCodes;
		this.variableTypes = variableTypes;
		this.primaryCol = primaryCol;
		this.trackerCol = trackerCol;
		this.varAttrConfigMap = valueAttrMap;
	}
	
	/**
	 * Returns the name of the database connection to be used 
	 * to construct Point 
	 * @return
	 */
	public String getDbConnectionName() {
		return dbConnectionName;
	}
	
	/**
	 * Retursn the map of constant names and their values to be
	 * set in the point
	 * @return
	 */
	public Map<String, String> getConstants() {
		return constants;
	}
	
	/**
	 * Returns the Value Codes and COlumn maps for this point.
	 * (Eg. HILIM,VAL sign code points and the columns to fetch information
	 * for these sign codes)
	 * @return
	 */
	public Map<String, ValueVarConfig> getValueCodeMap() {
		return valueCodes;
	}
	
	/**
	 * Return the Point Variables to be set and their details 
	 * @return
	 */
	public Map<String, PointVarConfig> getPtVarConfigMap() {
		return variableTypes;
	}
	
	/**
	 * Return the primary column on which TPO databases are to be queried.
	 * @return
	 */
	public String getIdentifierColName(){
		return primaryCol;
	}

	/**
	 * Return the column name for the TPO tracker databases.
	 * @return
	 */
	public String getTrackerColName() {
		return trackerCol;
	}

	/**
	 * Return the databases to track the ids of the send points
	 * @return
	 */
	public String getTrackerDBConName() {
		return trackerDBConName;
	}

	/**
	 * Return the Value Attributes to be set for values inside this Point
	 * @return
	 */
	public Map<String, ValueAttrConfig> getValueAttrConfig() {
		return varAttrConfigMap;
	}

	private String dbConnectionName;
	private String trackerDBConName;
	private String primaryCol;
	private String trackerCol;
	private Map<String, ValueAttrConfig> varAttrConfigMap;
	private Map<String, String> constants;
	private Map<String, ValueVarConfig> valueCodes;
	private Map<String, PointVarConfig> variableTypes;
}
