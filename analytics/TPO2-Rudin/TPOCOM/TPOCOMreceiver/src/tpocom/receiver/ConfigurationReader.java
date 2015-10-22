package tpocom.receiver;

import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Configuration Reader takes the configuration file path and reads in all the 
 * settings required to run the TPOCOMreceiver. It provides API to access different
 * settings mentioned in the config file. 
 * 
 */
public class ConfigurationReader {

	public ConfigurationReader() {
		InitialContext ic=null;
		try {
			ic = new InitialContext();
		} catch (NamingException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		String configFilePath=null;
		try {
			configFilePath = (String)ic.lookup("java:comp/env/receiverConfigFilePath");
		} catch (NamingException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		File xmlFile = new File(configFilePath);
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = null;
		try {
			dBuilder = dbFactory.newDocumentBuilder();
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		}
		Document doc = null;
		try {
			doc = dBuilder.parse(xmlFile);
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		}
		doc.getDocumentElement().normalize();
		
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
			this.pointConfigList = new HashMap<String, InterestPoint>();
			NodeList pointConfigNodes = doc.getElementsByTagName("point_config");
			for(int i =0; i < pointConfigNodes.getLength(); i++){
				Element node = (Element)pointConfigNodes.item(i);
				String configName = node.getAttribute("name");
			
				//get db connection name
				String dbConName = node.getElementsByTagName("database").item(0).getTextContent();

				//populate constants' map
				Map<String, String> ptIdentifiersMap = new HashMap<String, String>();
				Element pointIdentifiersNode = (Element)node.getElementsByTagName("point_identifiers").item(0);
				NodeList identifierNodes = pointIdentifiersNode.getElementsByTagName("identifier");
				for(int j = 0 ; j < identifierNodes.getLength(); j++){
					Element constantNode = (Element)identifierNodes.item(j);
					ptIdentifiersMap.put(constantNode.getAttribute("name"),constantNode.getTextContent());
				}
			
				//populate variables and their types
				Map<String, String> pointColumnMap = new HashMap<String, String>();
				Element pcmNode = (Element)node.getElementsByTagName("point_column_map").item(0);
				NodeList pcms = pcmNode.getElementsByTagName("column");
				for(int j = 0 ; j < pcms.getLength(); j++){
					Element variableNode = (Element)pcms.item(j);
					String ptAttrName = variableNode.getAttribute("name");
					String colName = variableNode.getTextContent();
					pointColumnMap.put(ptAttrName,colName);
				}
				this.pointConfigList.put(configName, new InterestPoint(dbConName,
						ptIdentifiersMap, pointColumnMap));
			}
		}
	}

	/**
	 * Returns a map of the databases(db) specified for the TPOCOM receiver.
	 * 
	 * @return A map with db name as key and db details as value
	 */	
	public Map<String, DbDetail> getDbMap() {
		return dbMap;
	}
	
	/**
	 * Returns a map of the Point types receiver is interested in
	 * @return
	 */
	public Map<String, InterestPoint> getPointConfigList() {
		return pointConfigList;
	}


	private Map<String, DbDetail> dbMap;
	private Map<String, InterestPoint> pointConfigList;
}
