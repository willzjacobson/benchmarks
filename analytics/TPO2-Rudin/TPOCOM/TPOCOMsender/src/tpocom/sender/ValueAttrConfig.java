package tpocom.sender;

/**
 * This class is designed to keep the various attributes of
 * a Value object and there datatype. 
 * @author vivek
 *
 */
public class ValueAttrConfig {

	public ValueAttrConfig( String valueDataType, String valueAttrName) {
		this.valueDataType = valueDataType;
		this.valueAttrName = valueAttrName;
	}
	
	/**
	 * Get the Value attribute data type
	 * @return
	 */
	public String getValueDataType() {
		return valueDataType;
	}

	/**
	 * Get the Value attribute name
	 * @return
	 */
	public String getValueAttrName() {
		return valueAttrName;
	}

	private String valueDataType;
	private String valueAttrName;
}
