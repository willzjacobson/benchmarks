package tpocom.sender;

public class ValueVarConfig {


	public ValueVarConfig(String valueCode, String outputDataType) {
		this.valueCode = valueCode;
		this.outputDataType = outputDataType;
	}

	public String getValueCode() {
		return valueCode;
	}

	public String getOutputDataType() {
		return outputDataType;
	}

	private String valueCode;
	private String outputDataType;
}

