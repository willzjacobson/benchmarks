package spms.run.rudin.xmltool;

import org.apache.log4j.Logger;



public class Constants {
	
	private static Logger log = Logger.getLogger(Constants.class);
	
	static public enum PointType { 
		
		ALARM, 
		COMMAND, 
		LOG, 
		MEASURE, 
		SERVICE, 
		STATUS; 
	
		static public PointType getPointType(String string) {
			
			log.trace("Enum Type - Method getType");
			log.trace("Enum Type - Parameter string = "+string);
			
			if (string.compareToIgnoreCase("alarm")==0) return ALARM;
			if (string.compareToIgnoreCase("command")==0) return COMMAND;
			if (string.compareToIgnoreCase("log")==0) return LOG;
			if (string.compareToIgnoreCase("measure")==0) return MEASURE;
			if (string.compareToIgnoreCase("service")==0) return SERVICE;
			if (string.compareToIgnoreCase("status")==0) return STATUS;
			
			return null;
					
		}
		
		static public String getString(PointType type) {
			
			log.trace("Enum Type - Method getString");
			log.trace("Enum Type - Parameter type = "+type);
			
			switch (type) {
			
				case ALARM: return new String("alarm");
				case COMMAND: return new String("command");
				case LOG: return new String("log");
				case MEASURE: return new String("measure");
				case SERVICE: return new String("service");
				case STATUS: return new String("status");
				
			}
			
			return new String();
		}

	}
	static public enum ValueType { 
		
		VALUE_NO, 
		VALUE_TX;
	
		static public ValueType getValueType(String string) {
			
			log.trace("Enum ValueType - Method getValueType");
			log.trace("Enum ValueType - Parameter string = "+string);
			
			if (string.compareToIgnoreCase("NO")==0) return VALUE_NO;
			if (string.compareToIgnoreCase("TX")==0) return VALUE_TX;
			
			return null;
					
		}
		
		static public String getString(ValueType valueType) {
			
			log.trace("Enum ValueType - Method getString");
			log.trace("Enum ValueType - Parameter valueType = "+valueType);
			
			switch (valueType) {

				case VALUE_NO: return new String("NO");
				case VALUE_TX: return new String("TX");
				
			}
			
			return new String();
		}
	}
}
