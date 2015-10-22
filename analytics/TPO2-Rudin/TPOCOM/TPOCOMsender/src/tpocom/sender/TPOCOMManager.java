package tpocom.sender;

import java.io.IOException;
import java.rmi.RemoteException;
import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

import communicator.TPOCOMcommunicator;

import spms.run.rudin.xmltool.XmlToolException;

/**
 * TPOCOMManager is the main class that sets up the whole TPOCOM sender. 
 * It create and ties together the require objects and then starts the 
 * sender. 
 * @author vivek
 *
 */
public class TPOCOMManager {
	/**
	 * Constructor takes in the path to the configuration file
	 * @param configFilePath
	 */
	public TPOCOMManager(String configFilePath) {
		this.configFilePath = configFilePath;
	}
	
	/**
	 * Starts the TPOCOM sender
	 */
	public void start() {
		//create configuration Reader
		ConfigurationReader cfReader = null;
		try {
			cfReader = new ConfigurationReader(this.configFilePath);
			System.out.println("Configuration read successful");
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Create Connection Manager
		ConnectionManager conMan = null;
		try {
			conMan = new ConnectionManager(cfReader.getDbMap());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// Create Row to Point Converter
		RowPointConverter rpConverter = new RowPointConverter();
		
		// Create TPOCOM communication by giving all connection details.
		TPOCOMcommunicator tpocom = new TPOCOMcommunicator(
				cfReader.getSifEndpoint(), cfReader.getTpocomServerEndpoint(),
				cfReader.getTpocomSenderId(), cfReader.getTPOLocationId(),
				cfReader.getTpocomVersion(), cfReader.getTpocomTTLinMS(),
				cfReader.getSubscribePoints());
		
		// Creates the task Runner
		TaskRunner trunner = null;
		try {
			trunner = new TaskRunner(conMan, cfReader.getPointConfigList(),
					rpConverter, tpocom);
		} catch (RemoteException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (XmlToolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// Creates the heart beat ( keep - alive ) messenger
		HeartBeatMessenger hbm = new HeartBeatMessenger(tpocom);
		
		//Crate the TPOCOM Scheduler
		TPOCOMScheduler tScheduler = new TPOCOMScheduler(trunner, hbm, tpocom,
				cfReader.getPollInterval(), cfReader.getHeartBeatInterval());
		
		//Finally schedule the tasks.
		try {
			tScheduler.ScheduleRepeatTask();
		} catch (RemoteException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (XmlToolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		Runtime.getRuntime().addShutdownHook(
				new Thread(new ShutDownHandler(tScheduler, conMan, tpocom)));
	}

	private String configFilePath;

	/**
	 * Main method to launch the TPOCOM Sender
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length < 1) {
			System.out.println("Usage: java -jar TPOCOMsender.jar configFilePath");
			return;
		}
		TPOCOMManager tm = new TPOCOMManager(args[0]);
		tm.start();
	}

}
