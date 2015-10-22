package communicator;

import java.rmi.RemoteException;
import java.util.Date;
import java.util.List;
import java.util.Map;

import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.XmlToolException;
import tpo.adapter.client.impl.Wssb2Client;
import tpo.adapter.client.impl.Wssb2Client.MsgType;

import com.fin_sif.sb.types.Filter;
import com.fin_sif.sb.types.Filters;
import com.fin_sif.sb.types.ModeType;
import com.fin_sif.sb.types.Subscription;

/**
 * TPOCOMcommunicator manages communication to the SIF server using the TpoWSSB2_Client
 * @author vivek
 *
 */
public class TPOCOMcommunicator {
	/**
	 * Constructor takes in the below parameter to make connectino and send points to SIF
	 * @param sifEndpoint
	 * @param tpocomServerEndPoint
	 * @param senderId
	 * @param tpocomVersion
	 * @param ttlInMS
	 * @param subscriptionPoints
	 */
	public TPOCOMcommunicator(Map<String, String> sifEndpoint,
			Map<String, String> tpocomServerEndPoint,
			String senderId,
			String tpoLocationId,
			String tpocomVersion,
			int ttlInMS, 
			List<InternalSubscription> subscriptionPoints) {
		this.sifEndPoint = sifEndpoint;
		this.tpocomServerEndPoint = tpocomServerEndPoint;
		this.SenderId = senderId;
		this.tpoLocationId = tpoLocationId;
		this.tpocomVersion = tpocomVersion;
		this.ttlInMs = ttlInMS;
		this.subscriptionPoints = subscriptionPoints;
	}
	
	private String getSendTopicStr(MsgType msgtype){
		return msgtype.toString().toLowerCase()+"."+this.tpoLocationId;
	}
	
	private void registerAndSubscribe(String serviceURL, String subscriptionURL)
			throws XmlToolException, RemoteException {
		client = new Wssb2Client(serviceURL);

		// Create Subscription
		Subscription[] subscriptions = new Subscription[this.subscriptionPoints
				.size()];
		for (int i = 0; i < this.subscriptionPoints.size(); ++i) {
			String filter_name = this.subscriptionPoints.get(i).getFilter();
			Filter filter = client.createFilter(filter_name,
					new String[] { this.SenderId });
			Filters filters = client.createFilters(new Filter[] { filter },
					true, ModeType.QUERY);
			subscriptions[i] = client
					.createSubscription(this.subscriptionPoints.get(i)
							.getName(), subscriptionURL, MsgType
							.getMsgType(this.subscriptionPoints.get(i)
									.getType()), filters);
		}

		// Register client and subscribe
		client.registerAndSubscribe("", this.ttlInMs, 1, this.SenderId,
				subscriptions, this.tpocomVersion);
	}
	
	/**
	 * Closes the connection to the SIF server.
	 * @throws RemoteException
	 * @throws XmlToolException
	 */
	public void close() throws RemoteException, XmlToolException {
		client.unRegistered(this.SenderId);
		client = null;
		System.out.println("SIF connection closed");
	}
	
	/**
	 * Makes a connection to the SIF server.
	 */
	public void connect() throws RemoteException, XmlToolException {
		String sifHost = this.sifEndPoint.get("host");
		String sifPort = this.sifEndPoint.get("port");
		String sifPath = this.sifEndPoint.get("path");
		String serviceURL = "http://" + sifHost + ":" + sifPort + "/" + sifPath;

		String tpocomHost = this.tpocomServerEndPoint.get("host");
		String tpocomPort = this.tpocomServerEndPoint.get("port");
		String tpocomPath = this.tpocomServerEndPoint.get("path");
		String subscriptionURL = "http://" + tpocomHost + ":" + tpocomPort
				+ "/" + tpocomPath;
		this.registerAndSubscribe(serviceURL, subscriptionURL);
		System.out.println("SIF connection established");
	}
	
	/**
	 * Sends a message to the SIF to keep the connection Alive
	 * @throws RemoteException
	 * @throws XmlToolException
	 */
	public void keepALive() throws RemoteException, XmlToolException {
		this.client.keepAlive(this.SenderId, 1);
	}
	
	/**
	 * Sends the list of points of given type to SIF. Currently, used a ttl of 
	 * 0 - Indefinite retries.
	 * @param points
	 * @param type
	 * @throws RemoteException
	 * @throws XmlToolException
	 */
	public void sendPoints(List<Point> points, MsgType type) throws RemoteException,
			XmlToolException {
		Date d = new Date();
		client.sendOnMessageAndResponse(points, this.SenderId, d, d, getSendTopicStr(type),
				1, 1, 0, type);
	}

	private Map<String, String> sifEndPoint;
	private Map<String, String> tpocomServerEndPoint;
	private String SenderId;
	private String tpoLocationId;
	private String tpocomVersion;
	private int ttlInMs;
	private Wssb2Client client;
	private List<InternalSubscription> subscriptionPoints;
}
