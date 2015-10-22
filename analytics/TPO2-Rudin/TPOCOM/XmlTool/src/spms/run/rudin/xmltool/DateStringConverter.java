package spms.run.rudin.xmltool;

import java.text.DateFormat;
import java.text.FieldPosition;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

import org.apache.log4j.Logger;

public class DateStringConverter {
	
	private static Logger log = Logger.getLogger(DateStringConverter.class);
	
	
	static public enum DateStringFormat {

		ISO8601_LOCAL_TIME,
		ISO8601_LOCAL_TIME_NO_SSS,
		ISO8601_LOCALIZATION,
		NON_ISO8601_LOCALIZATION,
		ON_MESSAGE_HEADER_FORMAT;

	}	
	
	static public String getDateStringFormat(DateStringFormat dateStringFormat) {
		
		log.debug("Method getDateStringFormat");
		log.debug("Parameter dateStringFormat = "+dateStringFormat);
		
		switch (dateStringFormat) {
		
			case ISO8601_LOCAL_TIME: return new String("yyyy-MM-dd'T'HH:mm:ss.SSS");
			case ISO8601_LOCAL_TIME_NO_SSS: return new String("yyyy-MM-dd'T'HH:mm:ss");		
			case ISO8601_LOCALIZATION: return new String("yyyy-MM-dd'T'HH:mm:ss.SSSZ");
			case NON_ISO8601_LOCALIZATION: return new String("yyyy-MM-dd'T'HH:mm:ss.SSS' 'Z");
			case ON_MESSAGE_HEADER_FORMAT: return new String("yyyy/MM/dd HH:mm:ss.SSS");
			
		}
		
		return new String();
	}

	public static Date String2Date2(String string, String format) throws ParseException {
		
		log.debug("Method String2Date");
		log.debug("Parameter string = "+string);
		log.debug("Parameter format = "+format);
		
		DateFormat dateFormat = new SimpleDateFormat(format);
		Date date = null;
		
		dateFormat.setLenient(false);
		date = dateFormat.parse(string);
		
		return date;
	}
	
	public static String Date2String(Date date, String format) {
		
		log.debug("Method Date2String");
		log.debug("Parameter date = "+date);
		log.debug("Parameter format = "+format);
		
		SimpleDateFormat dateFormat = new SimpleDateFormat(format);
		return dateFormat.format(date, new StringBuffer(), new FieldPosition(0)).toString();		
	}

	public static String Date2StringTimeZone(Date date, String format,TimeZone timeZone) {
		
		log.debug("Method Date2String");
		log.debug("Parameter date = "+date);
		log.debug("Parameter format = "+format);

		Calendar cal=Calendar.getInstance(timeZone);
		cal.setTime(date);
		date =cal.getTime();
		SimpleDateFormat dateFormat = new SimpleDateFormat(format);
		dateFormat.setTimeZone(timeZone);
		return dateFormat.format(date, new StringBuffer(), new FieldPosition(0)).toString();		
	}
	
	public static Date String2Date(String string) throws ParseException {
		return String2DateTimeZone(string, TimeZone.getDefault());
	}
	
	public static Date String2DateTimeZone(String string, TimeZone timeZone) throws ParseException {
		
		log.debug("Method String2Date");
		log.debug("Parameter string = "+string);
		log.debug("Parameter timeZone = "+timeZone);
		
		DateFormat dateFormat = 
				new SimpleDateFormat(
						DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME));
		dateFormat.setTimeZone(timeZone);
		dateFormat.setLenient(false);

		Date date = null;
		try {
			
			date = dateFormat.parse(string);

			
		} catch (ParseException parseException_LocalTime) {

			dateFormat = 
					new SimpleDateFormat(
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME_NO_SSS));
			dateFormat.setTimeZone(timeZone);
			dateFormat.setLenient(false);
			
			try {
				
				date = dateFormat.parse(string);
			
				
			} catch (ParseException parseException_LocalTime_No_SSS) {

				dateFormat = 
						new SimpleDateFormat(
								DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCALIZATION));
				dateFormat.setTimeZone(timeZone);
				dateFormat.setLenient(false);

				try {
					
					date = dateFormat.parse(string);
				
					
				} catch (ParseException parseException_Localization) {
	
					dateFormat = 
							new SimpleDateFormat(
									DateStringConverter.getDateStringFormat(DateStringFormat.NON_ISO8601_LOCALIZATION));
					dateFormat.setTimeZone(timeZone);
					dateFormat.setLenient(false);
					
					date = dateFormat.parse(string);
					
				}
				
			}
			
		}
		
		return date;
	}

	
}
