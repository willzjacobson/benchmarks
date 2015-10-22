package spms.run.rudin.xmltool;

public class XmlToolException extends Exception {

	private static final long serialVersionUID = 5608247331458732975L;

	public static final String TYPE_MISMATCH_OUTPUT_VALUE = "Type mismatch output value";
	public static final String MISSED_VALUE_IN_LOB = "Missed value in lob";
	public static final String MISSED_DETAIL_IN_LOB = "Missed detail in lob";
	public static final String MISSED_LOB = "Missed lob";
	public static final String MISSED_ATTRIBUTE_IN_VALUE = "Missed attribute refts in value";
	public static final String BAD_VALUE_TYPE = "Bad type of value";
	public static final String TOO_VALUES = "Too values in lob";
	public static final String NO_VALUES = "No value in lob";
	public static final String MISSED_PRIO = "Missed alarm_Prio";
	public static final String MISSED_STATE = "Missed alarm_State";

	
	public XmlToolException(String msg) { super(msg); }

	
}
