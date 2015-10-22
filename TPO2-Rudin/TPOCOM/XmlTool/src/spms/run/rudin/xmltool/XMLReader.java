package spms.run.rudin.xmltool;

import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;
import org.jdom2.Attribute;
import org.jdom2.DataConversionException;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;



public class XMLReader {
	
	private static Logger log = Logger.getLogger(XMLReader.class);
	

	static private String getXSDSchemaPath() {
		
		return new String("xsd_schemas");
	}
	
	static private String getXSDFileExt() {
				
		return new String("xsd");
	}
	
	static private String getPropertyNameForXSDValidation() {
		
		return new String("http://apache.org/xml/properties/schema/external-noNamespaceSchemaLocation");
	}
	
	
	static private Iterator<Element> parseCommonElements(Element root, Point point) throws ParseException {
		
		log.trace("Method parseCommonElements");
		
		List<Element> rootChildren = root.getChildren();
	
		Iterator<Element> iterator = rootChildren.iterator();
		Element element = iterator.next();
			
		String attributeValue = element.getAttributeValue("realtime");
		point.setRealtime(attributeValue);
		attributeValue = element.getAttributeValue("bad");
		if(attributeValue!=null)
			point.setBad(attributeValue.equals("1"));
		else
			point.setBad(false);
		element =  iterator.next();
		
		String elementValue = element.getValue();	
		Date date = 
				DateStringConverter.String2Date(elementValue);
		
		point.setTs(date);
		
		element = iterator.next();
		

		point.setPbs_Loc_A1(element.getAttributeValue("a1"));
		point.setPbs_Loc_A2(element.getAttributeValue("a2"));
		point.setPbs_Loc_A3(element.getAttributeValue("a3"));
		point.setPbs_Loc_A4(element.getAttributeValue("a4"));
		point.setPbs_Sys_T(element.getAttributeValue("t"));
		point.setPbs_Sys_S(element.getAttributeValue("s"));
		point.setPbs_Eq_L1(element.getAttributeValue("l1"));
		point.setPbs_Eq_L2(element.getAttributeValue("l2"));
		point.setPbs_Eq_L3(element.getAttributeValue("l3"));
		point.setPbs_Eq_n(element.getAttributeValue("n"));
		point.setPbs_Native(element.getAttributeValue("native"));
		
		
		elementValue = element.getValue();
		point.setPbs(elementValue);

		element = iterator.next();
		
		attributeValue = element.getAttributeValue("code");
		point.setSign_Code(attributeValue);
		attributeValue = element.getAttributeValue("prog");
		point.setSign_Prog(attributeValue);
		
		element = iterator.next();
		
		if (element.getName().equalsIgnoreCase("refts")) {
		
			elementValue = element.getValue();	
			date = DateStringConverter.String2Date(elementValue);
			
			point.setRefTs(date);
			
			element = iterator.next();
		
		}		
		
		
		if (element.getName().equalsIgnoreCase("mobile")) {
			
			attributeValue = element.getAttributeValue("TID");
			point.setMobile_Tid(attributeValue);
			attributeValue = element.getAttributeValue("CB");
			point.setMobile_Cb(attributeValue);
			attributeValue = element.getAttributeValue("DID");
			point.setMobile_Did(attributeValue);
		
			element =  iterator.next();
			
		}
		
		

		elementValue = element.getValue();	
		point.setSender(elementValue); 
		
		return iterator;
		
	}
	
	
	static private Iterator<Element> parseAlarmElements(Iterator<Element> iterator, Point point) throws XmlToolException, ParseException, DataConversionException {
		
		log.trace("Method parseAlarmElements");

		if (!iterator.hasNext()) return iterator;
		Element element = iterator.next();	

		String elementValue = element.getValue();
		point.setAlarm_State(Integer.parseInt(elementValue));

		element = iterator.next();
		
		String attributeValue = element.getAttributeValue("prio");
		point.setAlarm_Prio(Integer.parseInt(attributeValue));

		element = iterator.next();
		
		elementValue = element.getValue();
		Date date = DateStringConverter.String2Date(elementValue);
				
		point.setAlarm_Init_Ts(date);

		
		if (!iterator.hasNext()) return iterator;
		element = iterator.next();
				
		
		if (element.getName().equalsIgnoreCase("ackTs")) {
			
			elementValue = element.getValue();
			date = DateStringConverter.String2Date(elementValue);
			
			point.setAlarm_Ack_Ts(date);
			
			if (!iterator.hasNext()) return iterator;
			element = iterator.next();
			
		}			
			
		if (element.getName().equalsIgnoreCase("normTs")) {
			
			elementValue = element.getValue();
			date = DateStringConverter.String2Date(elementValue);
			
			point.setAlarm_Norm_Ts(date);
			
			if (!iterator.hasNext()) return iterator;
			element = iterator.next();
		}

		
		
// operator, role, console aren't to be saved
		

		if (element.getName().equalsIgnoreCase("operator")) {

			if (!iterator.hasNext()) return iterator;
			element = iterator.next();		
		}


		if (element.getName().equalsIgnoreCase("role")) {

			if (!iterator.hasNext()) return iterator;
			element = iterator.next();	
		}


		if (element.getName().equalsIgnoreCase("console")) {

			if (!iterator.hasNext()) return iterator;
			element = iterator.next();			
		}
		
				
		// lob
		if (element.getName().equalsIgnoreCase("lob"))  {

			Element detail = element.getChild("detail",element.getNamespace());
			if (detail!=null) {
				try {
					List<Value> values=new ArrayList<Value>();	
					Value value=new Value();
					value.setValue_No(Double.parseDouble(detail.getValue()));	
					values.add(value);
					point.setValues(values);				
				}
				catch (NumberFormatException numberFormatException) {					
					XmlToolException badValueType = new XmlToolException(XmlToolException.BAD_VALUE_TYPE);					
					throw badValueType;
				}
				
			}
		}

		
		Element pbs = element.getChild("pbs",element.getNamespace());
		if (pbs!=null) {
			
			List<Element> pbsChildren = pbs.getChildren();
			for (Element pbsChild : pbsChildren) 
				
				if (pbsChild.getAttribute("lang").getValue().equals("1")) {
				
					point.setLob_Pbs((pbsChild.getAttribute("value").getValue()));
					break;
					
				}
			
		}

		
		Element sign = element.getChild("sign",element.getNamespace());
		if (sign!=null) {
			
			List<Element> signChildren = sign.getChildren();
			for (Element signChild : signChildren) 
				
				if (signChild.getAttribute("lang").getValue().equals("1")) {
				
					point.setLob_Sign((signChild.getAttribute("value").getValue()));
					break;
					
				}
			
		}
		
		return iterator;
		
	}	
	
	
	static private Iterator<Element> parseMeasureElements(Iterator<Element> iterator, Point point) throws XmlToolException, ParseException, DataConversionException {
		
		log.trace("Method parseMeasureElements");

		if (!iterator.hasNext()) return iterator;
		Element element = iterator.next();
		
		// lob
		if (!element.getName().equalsIgnoreCase("lob"))  {
			
			XmlToolException missedLob = new XmlToolException(XmlToolException.MISSED_LOB);
			log.info("!element.getName().equalsIgnoreCase('lob')",missedLob);
			
			throw missedLob;

		} 

		List<Element> lobChildren = element.getChildren("value",element.getNamespace());
		Element detail = element.getChild("detail",element.getNamespace());
		Attribute sampAttr = (detail!=null?detail.getAttribute("samp"):null);
		
		int valuesChildrenNumber = lobChildren.size();
		if (valuesChildrenNumber==0) {
			
			XmlToolException missedValueInLob = new XmlToolException(XmlToolException.MISSED_VALUE_IN_LOB);
			log.info("valuesChildrenNumber==0",missedValueInLob);
			
			throw missedValueInLob;				
		}
		
		boolean areForecast = lobChildren.get(0).getAttribute("refts")!=null;
		if (areForecast&&sampAttr==null) {
			
			XmlToolException missedDetailInLob = new XmlToolException(XmlToolException.MISSED_DETAIL_IN_LOB);
			log.info("valuesChildrenNumber>1&&detail==null",missedDetailInLob);
			
			throw missedDetailInLob;				
		}
		
		Double delta=(sampAttr!=null?sampAttr.getDoubleValue():null);
		Long samp = (delta!=null?delta.longValue():null);
				
		point.setSamp(samp);
		
		List<Value> values= new ArrayList<Value>();
		
		for (int child=0;child<valuesChildrenNumber;child++) {

			Value value=new Value();
			if (areForecast) {
				String refts=lobChildren.get(child).getAttributeValue("refts");
				if (refts==null||refts.isEmpty()) {
					
					XmlToolException missedAttributeInValue = new XmlToolException(XmlToolException.MISSED_ATTRIBUTE_IN_VALUE);
					log.info("refts==null||refts.isEmpty()",missedAttributeInValue);
					
					throw missedAttributeInValue;				
				}
				
				Date date = 
						DateStringConverter.String2Date(refts);
				value.setRefTs(date);
			}
			String valueStr=lobChildren.get(child).getValue();
			Double dblValue = null;
			try {			
				dblValue = Double.parseDouble(valueStr);				
			}catch (NumberFormatException numberFormatException) {}
			if(dblValue==null)
				value.setValue_Tx(valueStr);
			else
				value.setValue_No(dblValue);
			values.add(value);
		}
		point.setValues(values);
		return iterator;
		
	}	

	static private Iterator<Element> parseStatusElements(Iterator<Element> iterator, Point point) throws XmlToolException, ParseException, DataConversionException {
		
		log.trace("Method parseStatusElements");

		
		if (!iterator.hasNext()) return iterator;
		Element element = iterator.next();
		
		// lob
		if (!element.getName().equalsIgnoreCase("lob"))  {
			
			XmlToolException missedLob = new XmlToolException(XmlToolException.MISSED_LOB);
			log.info("!element.getName().equalsIgnoreCase('lob')",missedLob);
			
			throw missedLob;

		} 

		Element lobChild = element.getChild("value",element.getNamespace());
		
		if (lobChild==null) {
			
			XmlToolException missedValueInLob = new XmlToolException(XmlToolException.MISSED_VALUE_IN_LOB);
			log.info("lobChildren==null",missedValueInLob);
			
			throw missedValueInLob;				
		}
		
		String card = lobChild.getAttributeValue("card");
		List<Value> values=new ArrayList<Value>();		
		switch (Integer.parseInt(card)) {
		
			case 1:
				element = lobChild.getChild("valU",element.getNamespace());
				if (element==null) {
					
					XmlToolException missedValueInLob = new XmlToolException(XmlToolException.MISSED_VALUE_IN_LOB);
					log.info("lobChild.getChild('valU',element.getNamespace())",missedValueInLob);
					
					throw missedValueInLob;				
				}
				Value valueTx=new Value();
				valueTx.setValue_Tx(element.getValue());
				values.add(valueTx);
				point.setValues(values);
				
				return iterator;
				
			case 2:
				element = lobChild.getChild("valB",element.getNamespace());
				if (element==null) {
					
					XmlToolException missedValueInLob = new XmlToolException(XmlToolException.MISSED_VALUE_IN_LOB);
					log.info("lobChild.getChild('valB',element.getNamespace())",missedValueInLob);
					
					throw missedValueInLob;				
				}
				Value valueBool=new Value();
				valueBool.setValue_Bool(element.getValue().equals("1"));
				values.add(valueBool);
				point.setValues(values);

				return iterator;
				
			default:
				element = lobChild.getChild("valN",element.getNamespace());
				if (element==null) {
					
					XmlToolException missedValueInLob = new XmlToolException(XmlToolException.MISSED_VALUE_IN_LOB);
					log.info("lobChild.getChild('valN',element.getNamespace())",missedValueInLob);
					
					throw missedValueInLob;				
				}
				Value valueNo=new Value();
				try {
					valueNo.setValue_No(Double.parseDouble(element.getValue()));}
				catch (NumberFormatException numberFormatException) {
					
					XmlToolException badValueType = new XmlToolException(XmlToolException.BAD_VALUE_TYPE);
					log.info("dblValue = Double.parseDouble(element.getValue())",badValueType);
					
					throw badValueType;				
					
				}
				values.add(valueNo);
				point.setValues(values);

				return iterator;
		
		}

		
	}	


	public static Point parse(String xmlMessage) throws IOException, ParseException, XmlToolException, DataConversionException {
		
		log.debug("Method parse");
		log.debug("Parameter xmlMessage = "+xmlMessage);

		xmlMessage=xmlMessage.replace("<![CDATA[", "");
		xmlMessage=xmlMessage.replace("]]>", "");
		
		Point point = new Point();

		SAXBuilder saxBuilder = new SAXBuilder();
		Document document = null;
		try {
			
			document = saxBuilder.build(new StringReader(xmlMessage));
		
		} catch (JDOMException jdomException) {
			
			log.error("saxBuilder.build(new StringReader(xmlMessage))",jdomException);
			return point;
			
		}
		
		String rootName = document.getRootElement().getName().toString();
		saxBuilder.setProperty(
				getPropertyNameForXSDValidation(), 
				new File(
						getXSDSchemaPath().concat(
						File.separator).concat(
						rootName).concat(
						".").concat(
						getXSDFileExt())
						)
				);
	
		try {
			
			document = saxBuilder.build(new StringReader(xmlMessage));
		
		} catch (JDOMException jdomException) {
			
			log.error("saxBuilder.build(new StringReader(xmlMessage))",jdomException);
			return point;
		}
		
		
		Element root = document.getRootElement();
		
		point.setPoint_Type(rootName);
		
		Iterator<Element> iterator = parseCommonElements(root,point);
		
		switch (Constants.PointType.getPointType(rootName)) {
		
			case ALARM:
				parseAlarmElements(iterator,point);
				break;
			
			case MEASURE:
				parseMeasureElements(iterator,point);
				break;
				
			case STATUS:
				parseStatusElements(iterator,point);
				break;
				
			default:
				
		}

		return point;		
	}

}
