package tpocom.sender;

/**
 * This class has the details of the variables of the Point 
 * It has the attribute name and the datatype 
 * @author vivek
 *
 */
public class PointVarConfig {

	public PointVarConfig(String ptAttrName, String pointVarType) {
		this.ptAttrName = ptAttrName;
		this.pointVarType = pointVarType;
	}
	
	/**
	 * Returns the Point Variable Name
	 * @return
	 */
	public String getPointAttrName() {
		return ptAttrName;
	}

	/**
	 * Returns the datatype of the point variable
	 * @return
	 */
	public String getPointVarType() {
		return pointVarType;
	}

	private String ptAttrName;
	private String pointVarType;
}
