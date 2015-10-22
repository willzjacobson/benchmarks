package tpocom.sender;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

import communicator.InternalSubscription;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Configuration Reader takes the configuration file path and reads in all the 
 * settings required to run the TPOCOMSENDER. It provides API to access different
 * settings mentioned in the config file. 
 * 
 */
public class ConfigurationReader {
	/**
	 * The constructor takes in the config file path for TPOCOM sender, parses it and 
	 * returns an object of ConfigurationReader which can be used to get different settings 
	 * for TPOCOM sender  
	 * @param configFilePath  - absolute file path for the TPOCOM sender config file. 
	 * @throws ParserConfigurationException
	 * @throws SAXException
	 * @throws IOException
	 */
	public ConfigurationReader(String configFilePath)
			throws ParserConfigurationException, SAXException, IOException {
		File xmlFile = new File(configFilePath);
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		Document doc = dBuilder.parse(xmlFile);
		doc.getDocumentElement().normalize();
		
		//load poll interval
		{
			this.pollInterval = Integer.parseInt(doc.getElementsByTagName("tpo_db_poll_interval_seconds").item(0).getTextContent());
		}
		
		//load sender id, tpocom version and tpocom ttl and heart beat interval
		{
			this.tpocomSenderId = doc.getElementsByTagName("tpo_sender_id").item(0).getTextContent();
			this.tpocomLocationId = doc.getElementsByTagName("tpo_location_id").item(0).getTextContent();
			this.tpocomTTLinMS = Integer.parseInt(doc.getElementsByTagName("tpocom_ttl_ms").item(0).getTextContent());
			this.tpocomVersion = doc.getElementsByTagName("tpocom_version").item(0).getTextContent();
			this.heartBeatInterval = Integer.parseInt(doc.getElementsByTagName("tpocom_heart_beat_interval_sec").item(0).getTextContent());
		}
		
		//load all the points to be subscribed
		{
			this.subscribePoints = new ArrayList<InternalSubscription>();
			Element subsPointsNode = (Element) (doc
					.getElementsByTagName("tpocom_subscription").item(0));
			NodeList subsPointsList = subsPointsNode
					.getElementsByTagName("point");
			for (int i = 0; i < subsPointsList.getLength(); i++) {
				String type = ((Element) subsPointsList.item(i))
						.getAttribute("type");
				String name = ((Element) (subsPointsList.item(i)))
						.getElementsByTagName("subscription_name").item(0)
						.getTextContent();
				String filter = ((Element) (subsPointsList.item(i)))
						.getElementsByTagName("filter").item(0)
						.getTextContent();
				this.subscribePoints.add(new InternalSubscription(type, name, filter));
			}
		}
		
		//sif endpoint details
		{
			this.sifEndpoint = new HashMap<String, String>();
			Element sifConfigEle = (Element) doc.getElementsByTagName("sif_endpoint").item(0);
			String host = sifConfigEle.getElementsByTagName("host").item(0).getTextContent();
			String port = sifConfigEle.getElementsByTagName("port").item(0).getTextContent();
			String path = sifConfigEle.getElementsByTagName("path").item(0).getTextContent();
			this.sifEndpoint.put("host", host);
			this.sifEndpoint.put("port", port);
			this.sifEndpoint.put("path", path);
		}

		//tpocom server endpoint details
		{
			this.tpocomServerEndpoint = new HashMap<String, String>();
			Element sifConfigEle = (Element) doc.getElementsByTagName("tpo_receiver_endpoint").item(0);
			String host = sifConfigEle.getElementsByTagName("host").item(0).getTextContent();
			String port = sifConfigEle.getElementsByTagName("port").item(0).getTextContent();
			String path = sifConfigEle.getElementsByTagName("path").item(0).getTextContent();
			this.tpocomServerEndpoint.put("host", host);
			this.tpocomServerEndpoint.put("port", port);
			this.tpocomServerEndpoint.put("path", path);
		}
		
		//populate all the database lists in the map
		{
			this.dbMap = new HashMap<String, DbDetail>();
			NodeList dbConfigNodes = doc.getElementsByTagName("database_config");
			for(int i=0; i <dbConfigNodes.getLength(); i++){
				Element node = (Element)dbConfigNodes.item(i);
				String name = node.getAttribute("name");
				String host = node.getElementsByTagName("host").item(0).getTextContent();
				String port = node.getElementsByTagName("port").item(0).getTextContent();
				String database = node.getElementsByTagName("database").item(0).getTextContent();
				String table = node.getElementsByTagName("table").item(0).getTextContent();
				String user = node.getElementsByTagName("user").item(0).getTextContent();
				String passwd = node.getElementsByTagName("password").item(0).getTextContent();
				dbMap.put(name, new DbDetail(host, port, database, table, user, passwd));
			}
		}
		
		//populate the point configurations
		{
			this.pointConfigList = new HashMap<String, PointConfig>();
			NodeList pointConfigNodes = doc.getElementsByTagName("point_config");
			for(int i =0; i < pointConfigNodes.getLength(); i++){
				Element node = (Element)pointConfigNodes.item(i);
				String configName = node.getAttribute("name");
			
				//get db connection name
				String dbConName = node.getElementsByTagName("database").item(0).getTextContent();
				
				//get tracker db connection name
				String trackerDbConName  = node.getElementsByTagName("send_tracker_database").item(0).getTextContent();
			
				//get timestamp file name
				String primaryCol = node.getElementsByTagName("primary_column").item(0).getTextContent();
				String tracker_column = node.getElementsByTagName("tracker_column").item(0).getTextContent();
				
				//populate information about point constants
				Map<String, String> constantsMap = new HashMap<String, String>();
				Element pointConstantsNode = (Element)node.getElementsByTagName("point_constants").item(0);
				NodeList contantNodes = pointConstantsNode.getElementsByTagName("constant");
				for(int j = 0 ; j < contantNodes.getLength(); j++){
					Element constantNode = (Element)contantNodes.item(j);
					constantsMap.put(constantNode.getAttribute("pointName"),constantNode.getTextContent());
				}
				
				//populate information about point variables 
				Map<String, PointVarConfig> variableTypesMap = new HashMap<String, PointVarConfig>();
				Element variableTypesNode = (Element)node.getElementsByTagName("point_variables").item(0);
				NodeList variableNodes = variableTypesNode.getElementsByTagName("variable");
				for(int j = 0 ; j < variableNodes.getLength(); j++){
					Element variableNode = (Element)variableNodes.item(j);
					String colName = variableNode.getAttribute("colName");
					String pointDataType = variableNode.getAttribute("pointDataType");
					String ptAttrName = variableNode.getTextContent();
					variableTypesMap.put(colName,new PointVarConfig(ptAttrName,pointDataType));
				}
				
				//populate value codes
				Map<String, ValueVarConfig> valueCodeMap = new HashMap<String, ValueVarConfig>();
				Element valueCodesNode = (Element)node.getElementsByTagName("value_codes_AND_column_maps").item(0);
				NodeList columnNodes = valueCodesNode.getElementsByTagName("constant");
				for(int j = 0 ; j < columnNodes.getLength(); j++){
					Element ColumnNode = (Element)columnNodes.item(j);
					String colName = ColumnNode.getAttribute("colName");
					String valueDataType = ColumnNode.getAttribute("valueDataType");
					String valueCode = ColumnNode.getTextContent();
					valueCodeMap.put(colName,new ValueVarConfig(valueCode, valueDataType));
				}
				
				//populate value attributes
				Map<String, ValueAttrConfig> valueAttrMap = new HashMap<String, ValueAttrConfig>();
				Element valueAttrNodes = (Element)node.getElementsByTagName("value_attributes").item(0);
				variableNodes = valueAttrNodes.getElementsByTagName("variable");
				for(int j = 0 ; j < variableNodes.getLength(); j++){
					Element variableNode = (Element)variableNodes.item(j);
					String colName = variableNode.getAttribute("colName");
					String valueDataType = variableNode.getAttribute("valueDataType");
					String valueAttrName = variableNode.getTextContent();
					valueAttrMap.put(colName,new ValueAttrConfig(valueDataType, valueAttrName));
				}
							
				this.pointConfigList.put(configName, new PointConfig(dbConName, trackerDbConName,
						constantsMap, valueCodeMap, variableTypesMap,
						primaryCol, tracker_column, valueAttrMap));
			}
		}
		
	}
	
	/**
	 * Returns a map of the databases(db) specified for the TPOCOM sender. It is
	 * a common store and has information for both kind of dbs - db for tracking
	 * sent data and db for fetching data to be sent
	 * 
	 * @return A map with db name as key and db details as value
	 */
	public Map<String, DbDetail> getDbMap() {
		return dbMap;
	}
	
	/**
	 * Returns a map of the different Points to be sent by TPOCOM sender.
	 * @return A map with Point name as key and PointConfig as value
	 */
	public Map<String, PointConfig> getPointConfigList() {
		return pointConfigList;
	}
	
	/**
	 * Returns a map of Sif end point parameters. This is the point where the
	 * messages will be sent by TPOCOM sender
	 * 
	 * @return 
	 */
	public Map<String, String> getSifEndpoint() {
		return sifEndpoint;
	}

	/**
	 * Return a map of TPOCOM receiver end point parameters. This is the point
	 * where SIF will send messages to which TPOCOM is subscribed
	 * 
	 * @return
	 */
	public Map<String, String> getTpocomServerEndpoint() {
		return tpocomServerEndpoint;
	}
	
	/**
	 * Return the interval after which the TPO databases are to be polled for
	 * new data in seconds
	 * @return
	 */
	public int getPollInterval() {
		return pollInterval;
	}
	
	/**
	 * Return the Id with which TPOCOMsender should register itself with SIF
	 * @return
	 */
	public String getTpocomSenderId() {
		return tpocomSenderId;
	}
	
	/**
	 * Return the hierarchical location id string for TPO. 
	 * @return
	 */
	public String getTPOLocationId() {
		return tpocomLocationId;
	}
	
	/**
	 * Return the version number of TPOCOM
	 * @return
	 */
	public String getTpocomVersion() {
		return tpocomVersion;
	}
	
	/**
	 * Return the TPOCOM TTL in milli seconds
	 * @return
	 */
	public int getTpocomTTLinMS() {
		return tpocomTTLinMS;
	}

	/**
	 * Return the heart beat interval in seconds
	 * @return
	 */
	public int getHeartBeatInterval() {
		return heartBeatInterval;
	}

	/**
	 * Return list of subscriptions that TPO-COM should make.
	 * @return
	 */
	public List<InternalSubscription> getSubscribePoints() {
		return subscribePoints;
	}

	private Map<String, DbDetail> dbMap;
	private Map<String, String> sifEndpoint;
	private Map<String, String> tpocomServerEndpoint;
	private Map<String, PointConfig> pointConfigList;
	private int pollInterval;
	private String tpocomSenderId;
	private String tpocomLocationId;
	private String tpocomVersion;
	private int tpocomTTLinMS;
	private int heartBeatInterval;
	private List<InternalSubscription> subscribePoints;
}
