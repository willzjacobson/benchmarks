package spms.run.rudin.xmltool;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.Namespace;

import spms.run.rudin.xmltool.Constants.PointType;
import spms.run.rudin.xmltool.DateStringConverter.DateStringFormat;


public class XMLWriter {
	
	private static Logger log = Logger.getLogger(XMLWriter.class);

	
	static private String getNamespace() {
		
		log.trace("Method getNamespace");
		
		return new String("http://commons.fin-sif.com/types");
	}

	private static void buildStatusDocument(Document document, Point point) throws XmlToolException {
		
		log.trace("Method buildStatusDocument");
		
		Namespace namespace = document.getRootElement().getNamespace();
		Element root = document.getRootElement();
		
		Element element = new Element("quality");
		element.setAttribute("realtime", point.getRealtime());
		if(point.isBad()!=null)
			element.setAttribute("bad", (point.isBad()?"1":"0"));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("ts");
		element.setText(
				DateStringConverter.Date2String(
						point.getTs(),
						DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		
		element = new Element("pbs");
		element.setAttribute("a1", point.getPbs_Loc_A1());
		element.setAttribute("a2", point.getPbs_Loc_A2());
		element.setAttribute("a3", point.getPbs_Loc_A3());
		element.setAttribute("a4", point.getPbs_Loc_A4());
		element.setAttribute("t", point.getPbs_Sys_T());
		element.setAttribute("s", point.getPbs_Sys_S());
		element.setAttribute("l1", point.getPbs_Eq_L1());
		element.setAttribute("l2", point.getPbs_Eq_L2());
		element.setAttribute("l3", point.getPbs_Eq_L3());
		element.setAttribute("n", point.getPbs_Eq_n());
		if(point.getPbs_Native()!=null)
			element.setAttribute("native", point.getPbs_Native());
		element.setText(point.getPbs());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("sign");
		element.setAttribute("code", point.getSign_Code());
		element.setAttribute("prog", point.getSign_Prog());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		if(point.getRefTs()!=null){
			element = new Element("refts");
			element.setText(
					DateStringConverter.Date2String(
							point.getRefTs(),
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
			element.setNamespace(namespace);
			
			root.addContent(element);
		}
		
		element = new Element("sender");
		element.setText(point.getSender());
		element.setNamespace(namespace);
		
		root.addContent(element);
	
		element = new Element("lob");
		
		if(point.getValues().size()==0){
			log.error(XmlToolException.NO_VALUES);
			throw new XmlToolException(XmlToolException.NO_VALUES);
		}
		
		if(point.getValues().size()>1){
			log.error(XmlToolException.TOO_VALUES);
			throw new XmlToolException(XmlToolException.TOO_VALUES);
		}
		
		Value value = point.getValues().get(0);
		
		Element lobValue= new Element("value");
		
		if(value.isText()){
			lobValue.setAttribute("card","1");
			Element valU= new Element("valU");
			valU.setText(value.getValue_Tx());
			valU.setNamespace(namespace);
			lobValue.addContent(valU);
		}else if(value.isBoolean()){
			lobValue.setAttribute("card","2");
			Element valB= new Element("valB");
			valB.setText((value.getValue_Bool()?"1":"0"));
			valB.setNamespace(namespace);
			lobValue.addContent(valB);
		}else if(value.isNumber()){
			lobValue.setAttribute("card","3");
			Element valN= new Element("valN");
			valN.setText(String.valueOf(value.getValue_No().longValue()));
			valN.setNamespace(namespace);
			lobValue.addContent(valN);
		}else{
			log.error(XmlToolException.BAD_VALUE_TYPE);
			throw new XmlToolException(XmlToolException.BAD_VALUE_TYPE);
		}
		
		lobValue.setNamespace(namespace);		
		element.addContent(lobValue);
		
		element.setNamespace(namespace);		
		root.addContent(element);
		
	}

	private static void buildAlarmDocument(Document document, Point point) throws XmlToolException {
		
		log.trace("Method buildAlarmDocument");
		
		Namespace namespace = document.getRootElement().getNamespace();
		Element root = document.getRootElement();
		
		Element element = new Element("quality");
		element.setAttribute("realtime", point.getRealtime());
		if(point.isBad()!=null)
			element.setAttribute("bad", (point.isBad()?"1":"0"));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("ts");
		element.setText(
				DateStringConverter.Date2String(
						point.getTs(),
						DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		
		element = new Element("pbs");
		element.setAttribute("a1", point.getPbs_Loc_A1());
		element.setAttribute("a2", point.getPbs_Loc_A2());
		element.setAttribute("a3", point.getPbs_Loc_A3());
		element.setAttribute("a4", point.getPbs_Loc_A4());
		element.setAttribute("t", point.getPbs_Sys_T());
		element.setAttribute("s", point.getPbs_Sys_S());
		element.setAttribute("l1", point.getPbs_Eq_L1());
		element.setAttribute("l2", point.getPbs_Eq_L2());
		element.setAttribute("l3", point.getPbs_Eq_L3());
		element.setAttribute("n", point.getPbs_Eq_n());
		if(point.getPbs_Native()!=null)
			element.setAttribute("native", point.getPbs_Native());
		element.setText(point.getPbs());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("sign");
		element.setAttribute("code", point.getSign_Code());
		element.setAttribute("prog", point.getSign_Prog());
		element.setNamespace(namespace);
		
		root.addContent(element);
				
		element = new Element("sender");
		element.setText(point.getSender());
		element.setNamespace(namespace);
		
		root.addContent(element);
	
		if(point.getAlarm_State()==null){
			log.error(XmlToolException.MISSED_STATE);
			throw new XmlToolException(XmlToolException.MISSED_STATE);
		}	
		
		element = new Element("state");
		element.setText(String.valueOf(point.getAlarm_State()));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		if(point.getAlarm_Prio()==null){
			log.error(XmlToolException.MISSED_PRIO);
			throw new XmlToolException(XmlToolException.MISSED_PRIO);
		}			
			
		element = new Element("property");
		element.setAttribute("prio", String.valueOf(point.getAlarm_Prio()));
		element.setAttribute("internal", "0");
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		
		if (point.getAlarm_Init_Ts()!=null) {

			element = new Element("initTs");
			element.setText(
					DateStringConverter.Date2String(
							point.getAlarm_Init_Ts(),
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
			element.setNamespace(namespace);
	
			root.addContent(element);
			
		}

		if (point.getAlarm_Ack_Ts()!=null) {

			element = new Element("ackTs");
			element.setText(
					DateStringConverter.Date2String(
							point.getAlarm_Ack_Ts(),
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
			element.setNamespace(namespace);
			
			root.addContent(element);
			
		}
		
		if (point.getAlarm_Norm_Ts()!=null) {
		
			element = new Element("normTs");
			element.setText(
					DateStringConverter.Date2String(
							point.getAlarm_Norm_Ts(),
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
			element.setNamespace(namespace);
			
			root.addContent(element);
			
		}
		
		
		if (point.getValues()==null&&point.getLob_Pbs()==null&&point.getLob_Sign()==null)return;
		
		element = new Element("lob");

		if(point.getValues()!=null){
			
			if(point.getValues().size()==0){
				log.error(XmlToolException.NO_VALUES);
				throw new XmlToolException(XmlToolException.NO_VALUES);
			}
			
			if(point.getValues().size()>1){
				log.error(XmlToolException.TOO_VALUES);
				throw new XmlToolException(XmlToolException.TOO_VALUES);
			}
		
			Value value = point.getValues().get(0);
					
			if(value.isNumber()){
				Element lobChild = new Element("detail");
				lobChild.setText(value.getValue_No().toString());
				lobChild.setNamespace(namespace);
				element.addContent(lobChild);
			}else{
				log.error(XmlToolException.BAD_VALUE_TYPE);
				throw new XmlToolException(XmlToolException.BAD_VALUE_TYPE);
			}
		}
		

		if (point.getLob_Pbs()!=null) {
		
			Element lobChild = new Element("pbs");		
			Element pbsChild = new Element("name");
			
			// Localization will come by future developments
			pbsChild.setAttribute("lang", "1");
			pbsChild.setAttribute("value", point.getLob_Pbs());
			pbsChild.setNamespace(namespace);
	
			ArrayList<Element> pbsChildren = new ArrayList<Element>();
			pbsChildren.add(pbsChild);
			
			lobChild.addContent(pbsChildren);
			lobChild.setNamespace(namespace);
			
			element.addContent(lobChild);
			
		}
		

		if (point.getLob_Sign()!=null) {
		
			Element lobChild = new Element("sign");		
			Element signChild = new Element("name");
			
			// Localization will come by future developments
			signChild.setAttribute("lang", "1");
			signChild.setAttribute("value", point.getLob_Sign());
			signChild.setNamespace(namespace);
	
			ArrayList<Element> signChildren = new ArrayList<Element>();
			signChildren.add(signChild);
			
			lobChild.addContent(signChildren);
			lobChild.setNamespace(namespace);
			
			element.addContent(lobChild);
			
		}
		
		
		element.setNamespace(namespace);		
		root.addContent(element);
		
	}
	
	private static void buildMeasureDocument(Document document, Point point) throws XmlToolException {
		
		log.trace("Method buildMeasureDocument");

		Namespace namespace = document.getRootElement().getNamespace();
		Element root = document.getRootElement();
		
		Element element = new Element("quality");
		element.setAttribute("realtime", point.getRealtime());
		if(point.isBad()!=null)
			element.setAttribute("bad", (point.isBad()?"1":"0"));
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("ts");
		element.setText(
				DateStringConverter.Date2String(
						point.getTs(),
						DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
		element.setNamespace(namespace);
		
		root.addContent(element);
				
		element = new Element("pbs");
		element.setAttribute("a1", point.getPbs_Loc_A1());
		element.setAttribute("a2", point.getPbs_Loc_A2());
		element.setAttribute("a3", point.getPbs_Loc_A3());
		element.setAttribute("a4", point.getPbs_Loc_A4());
		element.setAttribute("t", point.getPbs_Sys_T());
		element.setAttribute("s", point.getPbs_Sys_S());
		element.setAttribute("l1", point.getPbs_Eq_L1());
		element.setAttribute("l2", point.getPbs_Eq_L2());
		element.setAttribute("l3", point.getPbs_Eq_L3());
		element.setAttribute("n", point.getPbs_Eq_n());
		if(point.getPbs_Native()!=null)
			element.setAttribute("native", point.getPbs_Native());
		element.setText(point.getPbs());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("sign");
		element.setAttribute("code", point.getSign_Code());
		element.setAttribute("prog", point.getSign_Prog());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		if(point.getRefTs()!=null){
			element = new Element("refts");
			element.setText(
					DateStringConverter.Date2String(
							point.getRefTs(),
							DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
			element.setNamespace(namespace);
			
			root.addContent(element);
		}
		
		element = new Element("sender");
		element.setText(point.getSender());
		element.setNamespace(namespace);
		
		root.addContent(element);
		
		element = new Element("lob");
		
		if(point.getSamp()!=null){
			Element lobDetail = new Element("detail");
			lobDetail.setAttribute("samp", String.valueOf(point.getSamp().doubleValue()));
			lobDetail.setNamespace(namespace);
			element.addContent(lobDetail);
		}
		
		List<Value> values = point.getValues();
		
		if(point.getValues().size()==0){
			log.error(XmlToolException.NO_VALUES);
			throw new XmlToolException(XmlToolException.NO_VALUES);
		}
		
		
		if(point.getValues().size()>100){
			log.error(XmlToolException.TOO_VALUES);
			throw new XmlToolException(XmlToolException.TOO_VALUES);
		}
		
		for(Value value:values){
			Element lobValue = new Element("value");
			if(value.isText()){
				lobValue.setText(value.getValue_Tx());
			}else if(value.isNumber()){
				lobValue.setText(String.valueOf(value.getValue_No()));
			}else{
				log.error(XmlToolException.BAD_VALUE_TYPE);
				throw new XmlToolException(XmlToolException.BAD_VALUE_TYPE);
			}
			if(value.getRefTs()!=null)
				lobValue.setAttribute("refts",DateStringConverter.Date2String(value.getRefTs(),DateStringConverter.getDateStringFormat(DateStringFormat.ISO8601_LOCAL_TIME)));
				
			lobValue.setNamespace(namespace);
			element.addContent(lobValue);
		}
		element.setNamespace(namespace);
		
		root.addContent(element);		
	}
	
	
	public static Document build(Point point) throws XmlToolException {
		
		log.debug("Method build");
		log.debug("Parameter point = "+point);
		String type=point.getPoint_Type();
		Document document = new Document();
		Element element = new Element(type);
		document.setRootElement(element);
		
		document.getRootElement().setNamespace(Namespace.getNamespace(getNamespace()));
		
		switch (PointType.getPointType(type)) {
		
		case ALARM:
			
			buildAlarmDocument(document,point);
			break;
			
		case STATUS:
				
			buildStatusDocument(document,point);
			break;
			
		case MEASURE:
			
			buildMeasureDocument(document,point);
			break;
			
		default:
			
			XmlToolException typeMismatchException = new XmlToolException(XmlToolException.TYPE_MISMATCH_OUTPUT_VALUE);
			log.info("type",typeMismatchException);
			
			throw typeMismatchException;
		
		}
		
		return document;
	
	}

}

