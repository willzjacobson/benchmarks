package tpocom.sender;

import java.rmi.RemoteException;

import communicator.TPOCOMcommunicator;

import spms.run.rudin.xmltool.XmlToolException;
/**
 * This Class is designed to send keep alive messages to the SIF server. 
 * This is necessary to keep the connection to SIF alive.
 * @author vivek
 *
 */
public class HeartBeatMessenger implements Runnable {

	public HeartBeatMessenger(TPOCOMcommunicator tpocom) {
		this.tpocom = tpocom;
	}

	@Override
	public void run() {
		try {
			this.tpocom.keepALive();
		} catch (RemoteException e) {
			e.printStackTrace();
			//SIF is unreachable. 
			//Try to re -connect once.
			//Next retry will happen during the next run of Heartbeat Messenger.
			try {
				this.tpocom.connect();
			} catch (RemoteException e1) {
				e1.printStackTrace();
			} catch (XmlToolException e1) {
				e1.printStackTrace();
			}
		} catch (XmlToolException e) {
			//This stage is reached when SIF restarts and we keep sending 
			//keep alive even after SIF forgets all subscriptions. 
			//There fore reconnect 
			e.printStackTrace();
			try {
				this.tpocom.connect();
			} catch (RemoteException e1) {
				e1.printStackTrace();
			} catch (XmlToolException e1) {
				e1.printStackTrace();
			}
		}
	}
	private TPOCOMcommunicator tpocom;
}
