package tpocom.sender;

import java.rmi.RemoteException;
import java.sql.SQLException;

import communicator.TPOCOMcommunicator;

import spms.run.rudin.xmltool.XmlToolException;

/**
 * This is a Class to handle the shutdown process of TPOCOM Sender.
 * 
 * @author vivek
 * 
 */
public class ShutDownHandler implements Runnable {
	
	/**
	 * Takes in the different systems which are to be shutdown -
	 * TPOCOMcommunicator, ConnectionManager, TPOCOMScheduler
	 * @param tScheduler
	 * @param conMan
	 * @param tpocom
	 */
	public ShutDownHandler(TPOCOMScheduler tScheduler,
			ConnectionManager conMan, TPOCOMcommunicator tpocom) {
		this.tScheduler = tScheduler;
		this.conMan = conMan;
		this.tpocom = tpocom;
	}

	@Override
	public void run() {
		System.out.println("Shutting down TPOCOMsender");
		tScheduler.StopScheduledTasks();
		try {
			conMan.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			tpocom.close();
		} catch (RemoteException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (XmlToolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private TPOCOMScheduler tScheduler;
	private ConnectionManager conMan;
	private TPOCOMcommunicator tpocom;
}
