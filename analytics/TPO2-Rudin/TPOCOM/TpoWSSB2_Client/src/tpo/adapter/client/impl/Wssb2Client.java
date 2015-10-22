package tpo.adapter.client.impl;

import java.rmi.RemoteException;
import java.util.Date;
import java.util.List;
import java.util.TimeZone;
import java.util.UUID;

import org.apache.axis2.AxisFault;
import org.apache.log4j.Logger;
import org.jdom2.Document;
import org.jdom2.output.Format;
import org.jdom2.output.XMLOutputter;

import spms.run.rudin.xmltool.DateStringConverter;
import spms.run.rudin.xmltool.DateStringConverter.DateStringFormat;
import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.XMLWriter;
import spms.run.rudin.xmltool.XmlToolException;



import com.fin_sif.sb.services.WSSB2Stub;
import com.fin_sif.sb.types.ComplexMsg;
import com.fin_sif.sb.types.Filter;
import com.fin_sif.sb.types.Filters;
import com.fin_sif.sb.types.ModeType;
import com.fin_sif.sb.types.OnMessageAndResponse;
import com.fin_sif.sb.types.OnMessageResponse;
import com.fin_sif.sb.types.OnMessageType;
import com.fin_sif.sb.types.SBKeepAlive;
import com.fin_sif.sb.types.SBRegisterAndSubscribe;
import com.fin_sif.sb.types.SBResponse;
import com.fin_sif.sb.types.SBUnRegister;
import com.fin_sif.sb.types.Subscription;


public class Wssb2Client {
	
	static private Logger log = Logger.getLogger(Wssb2Client.class);
	
	WSSB2Stub wssb2Stub;
	
	static public enum MsgType { 
		
		ALARM, 
		COMMAND, 
		LOG, 
		MEASURE, 
		SERVICE, 
		STATUS; 
	
		static public MsgType getMsgType(Integer integer) {
						
			if (integer.intValue()==1) return ALARM;
			if (integer.intValue()==2) return COMMAND;
			if (integer.intValue()==3) return LOG;
			if (integer.intValue()==4) return MEASURE;
			if (integer.intValue()==5) return SERVICE;
			if (integer.intValue()==6) return STATUS;
			
			return null;
					
		}
		
		static public MsgType getMsgType(String string) {
			
			
			if (string.compareToIgnoreCase("ALARM")==0) return ALARM;
			if (string.compareToIgnoreCase("COMMAND")==0) return COMMAND;
			if (string.compareToIgnoreCase("LOG")==0) return LOG;
			if (string.compareToIgnoreCase("MEASURE")==0) return MEASURE;
			if (string.compareToIgnoreCase("SERVICE")==0) return SERVICE;
			if (string.compareToIgnoreCase("STATUS")==0) return STATUS;
			
			return null;
					
		}
		
		static public Integer getInteger(MsgType msgType) {
			
			
			switch (msgType) {
			
			case ALARM: return Integer.valueOf(1);
			case COMMAND: return Integer.valueOf(2);
			case LOG: return Integer.valueOf(3);
			case MEASURE: return Integer.valueOf(4);
			case SERVICE: return Integer.valueOf(5);
			case STATUS: return Integer.valueOf(6);
				
			}
			
			return Integer.valueOf(-1);
		}

	}
	
	public Wssb2Client(String wssb2EndPoint) throws AxisFault {

		this.wssb2Stub = new WSSB2Stub(wssb2EndPoint);
	}
	
	
	private UUID generateUUID(Point point) {
		
		log.trace("Method generateUID");
		
		return UUID.nameUUIDFromBytes(
				
					(
						point.getPbs()+
						point.getSign_Code()+
						point.getSign_Prog()+
						String.valueOf(point.getTs().getTime())
					
					).getBytes()	
				
				);
	}
	
	private ComplexMsg generateComplexMsg(Point point) throws XmlToolException {
		
		log.debug("Method generateComplexMsg");
		log.debug("Parameter point = "+point);
		
		ComplexMsg complexMsg = new ComplexMsg();
		UUID uuid = generateUUID(point);
		
		Document document = XMLWriter.build(point);
		XMLOutputter xmlOutputter = new XMLOutputter(Format.getCompactFormat());
		
		complexMsg.setUUID(uuid.toString());
		String documentStr="<![CDATA["+xmlOutputter.outputString(document)+"]]>";
		complexMsg.setString(documentStr);
		
		log.debug("xmlMsg: "+documentStr);
		
		return complexMsg;
	}
	

	
	public void sendOnMessageAndResponse(List<Point> pointList,String senderId,Date receTs,Date sendTs,String topic,int prio,int seqNo,int ttlMsec,MsgType msgType) throws XmlToolException, RemoteException {

		OnMessageAndResponse onMessageAndResponse=new OnMessageAndResponse();
		OnMessageType onMessageType=new OnMessageType();
		String receTsStr=DateStringConverter.Date2StringTimeZone(receTs, DateStringConverter.getDateStringFormat(DateStringFormat.ON_MESSAGE_HEADER_FORMAT),TimeZone.getTimeZone("GMT"));
		onMessageType.setReceTS(receTsStr);
		onMessageType.setSenderID(senderId);
		String sendTsStr=DateStringConverter.Date2StringTimeZone(sendTs, DateStringConverter.getDateStringFormat(DateStringFormat.ON_MESSAGE_HEADER_FORMAT),TimeZone.getTimeZone("GMT"));
		onMessageType.setSendTS(sendTsStr);
		onMessageType.setSeqnum(seqNo);
		onMessageType.setPrio(prio);
		onMessageType.setTopic(topic);
		onMessageType.setTtlmsec(ttlMsec);
		onMessageType.setMsgType(MsgType.getInteger(msgType));
		ComplexMsg[] msgList=new ComplexMsg[pointList.size()];
		int i=0;
		for(Point point:pointList){
			ComplexMsg msg=generateComplexMsg(point);
			msgList[i]=msg;
			i++;
		}	
		onMessageType.setMsg(msgList);
		onMessageAndResponse.setOnMessageAndResponse(onMessageType);		
					
		OnMessageResponse onMessageResponse = this.wssb2Stub.onMessageAndResponse(onMessageAndResponse);
			
		if(onMessageResponse.getErrcode()!=0){
			log.error(onMessageResponse.getErrdesc());
			throw new XmlToolException(onMessageResponse.getErrdesc());
		}
		
		
	}
	
	public void keepAlive(String sender,int reachable) throws XmlToolException, RemoteException{

		SBKeepAlive sbKeepAlive = new SBKeepAlive();
		
		sbKeepAlive.setSenderID(sender);
		sbKeepAlive.setReachable(reachable);
		
		SBResponse sbResponse = this.wssb2Stub.sBkeepalive(sbKeepAlive);
			
		if(sbResponse.getErrcode()!=0){
			log.error(sbResponse.getErrdesc());
			throw new XmlToolException(sbResponse.getErrdesc());
		}
	}
	
	public void registerAndSubscribe(String e2eEndpoint, int keepalivemsec, int reachable, String senderId, Subscription[] subscriptions, String version) throws RemoteException, XmlToolException{
		SBRegisterAndSubscribe sBRegisterAndSubscribe = new SBRegisterAndSubscribe();
		
		sBRegisterAndSubscribe.setE2Eendpoint(e2eEndpoint);
		sBRegisterAndSubscribe.setKeepalivemsec(keepalivemsec);
		sBRegisterAndSubscribe.setReachable(reachable);
		sBRegisterAndSubscribe.setSenderID(senderId);
		sBRegisterAndSubscribe.setSubscriptions(subscriptions);
		sBRegisterAndSubscribe.setVersion(version);
		
		
		SBResponse sbResponse = this.wssb2Stub.sBregisterandsubscribe(sBRegisterAndSubscribe);

		if(sbResponse.getErrcode()!=0){
			log.error(sbResponse.getErrdesc());
			throw new XmlToolException(sbResponse.getErrdesc());
		}
	}
	
	public Subscription createSubscription(String topic,String endpoint,MsgType msgType){
			Subscription subscription=new Subscription();
			subscription.setTopic(topic);
			subscription.setMsgType(MsgType.getInteger(msgType));
			subscription.setEndpoint(endpoint);
		return subscription;
	}
	
	public Subscription createSubscription(String topic,String endpoint,MsgType msgType,Filters filters){
			Subscription subscription=new Subscription();
			subscription.setTopic(topic);
			subscription.setMsgType(MsgType.getInteger(msgType));
			subscription.setEndpoint(endpoint);
			subscription.setFilters(filters);
		return subscription;
	}
    
    public Filter createFilter(String xPathExpression,String[] values){
    	Filter filter = new Filter();
    	filter.setExpression(xPathExpression);
    	filter.setValue(values);
    	return filter;
    }
    
    public Filters createFilters(Filter[] filterList,boolean negated,ModeType modeType) throws XmlToolException{
    	if(filterList.length>4)throw new XmlToolException("The number of filters can not be greater than 4");
    	
    	Filters filters = new Filters();
    	filters.setFilter(filterList);
    	filters.setNegated(negated);
    	filters.setMode(modeType);
    	return filters;
    }
	
	public void unRegistered(String senderId) throws RemoteException, XmlToolException{
		SBUnRegister sbUnRegister=new SBUnRegister();
		sbUnRegister.setSenderID(senderId);
		
		SBResponse sbResponse = this.wssb2Stub.sBunregister(sbUnRegister);

		if(sbResponse.getErrcode()!=0){
			log.error(sbResponse.getErrdesc());
			throw new XmlToolException(sbResponse.getErrdesc());
		}
	}
}
