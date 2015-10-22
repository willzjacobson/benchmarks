package communicator;

import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.apache.axis2.AxisFault;

import com.fin_sif.sb.types.Filter;
import com.fin_sif.sb.types.Filters;
import com.fin_sif.sb.types.ModeType;
import com.fin_sif.sb.types.Subscription;


import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.Value;
import spms.run.rudin.xmltool.Constants.PointType;
import spms.run.rudin.xmltool.XmlToolException;
import tpo.adapter.client.impl.Wssb2Client;
import tpo.adapter.client.impl.Wssb2Client.MsgType;

public class WriteTest {

	/**
	 * @param args
	 * @throws XmlToolException 
	 * @throws RemoteException 
	 */
	public static void main(String[] args) {
		Wssb2Client client;
		try {
			client = new Wssb2Client("http://128.59.245.87:9080/axis2/services/WSSB2");
		} catch (AxisFault e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		}
		
		//filter to exclude your system (000TPO) in the subscription
		Filter filter=client.createFilter("measure/sender",new String[]{"000TPO"});
		Filters filters=null;
		try {
			filters=client.createFilters(new Filter[]{filter}, true, ModeType.QUERY);
		} catch (XmlToolException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
			return;
		}
		//---------------------------
		
		
		Subscription sub=client.createSubscription("measure", "http://anderson.ldeo.columbia.edu:8080/axis2/services/WSSB2", MsgType.MEASURE,filters);
		Subscription[] subscriptions=new Subscription[1];
		subscriptions[0]=sub;
		try {
			client.registerAndSubscribe("", 10000, 1, "000TPO", subscriptions, "1.0");
			System.out.println("subscribe ok");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		}
		Calendar cal=Calendar.getInstance();
		cal.add(Calendar.SECOND,-5);
		//create Point a.
		Point a=new Point();
		a.setTs(cal.getTime());
		a.setPoint_Type(PointType.getString(PointType.MEASURE));
		a.setBad(false);
		a.setRealtime("1");
		a.setPbs("345Z01F02CSW000TPOFORTEMSPA001");
		a.setPbs_Loc_A1("345");
		a.setPbs_Loc_A2("Z01");
		a.setPbs_Loc_A3("F02");
		a.setPbs_Loc_A4("CSW");
		a.setPbs_Sys_T("000");
		a.setPbs_Sys_S("TPO");
		a.setPbs_Eq_L1("FOR");
		a.setPbs_Eq_L2("TEM");
		a.setPbs_Eq_L3("SPA");
		a.setPbs_Eq_n("001");
		a.setPbs_Native("pippo");
		a.setSign_Code("VAL");
		a.setSign_Prog("001");
		a.setSender("000TPO");
		Value valA=new Value();
		valA.setValue_No(23.0);
		List<Value> valAlist=new ArrayList<Value>();
		valAlist.add(valA);
		a.setValues(valAlist);
		
		cal.add(Calendar.SECOND, 2);
		//create point b with 4 value and forecast timestamp. sampling=2000
		Point b=new Point();
		b.setPoint_Type(PointType.getString(PointType.MEASURE));
		b.setTs(cal.getTime());
		b.setBad(true);
		b.setRealtime("1");
		b.setPbs("345Z01F02CSW000TPOFORTEMSPA001");
		b.setPbs_Loc_A1("345");
		b.setPbs_Loc_A2("Z01");
		b.setPbs_Loc_A3("F02");
		b.setPbs_Loc_A4("CSW");
		b.setPbs_Sys_T("000");
		b.setPbs_Sys_S("TPO");
		b.setPbs_Eq_L1("FOR");
		b.setPbs_Eq_L2("TEM");
		b.setPbs_Eq_L3("SPA");
		b.setPbs_Eq_n("001");
		b.setPbs_Native("pippo");
		b.setSign_Code("VAL");
		b.setSign_Prog("001");
		b.setSender("000TPO");
		b.setSamp(new Long(2000));
		List<Value> valBlist=new ArrayList<Value>();
		Value valB1=new Value();
		valB1.setValue_No(24.0);
		cal.add(Calendar.HOUR, 5);
		valB1.setRefTs(cal.getTime());
		valBlist.add(valB1);
		Value valB2=new Value();
		valB2.setValue_No(33.0);
		cal.add(Calendar.HOUR, 5);
		valB2.setRefTs(cal.getTime());
		valBlist.add(valB2);
		Value valB3=new Value();
		valB3.setValue_No(43.0);
		cal.add(Calendar.HOUR, 5);
		valB3.setRefTs(cal.getTime());
		valBlist.add(valB3);
		Value valB4=new Value();
		valB4.setValue_No(53.0);
		cal.add(Calendar.HOUR, 5);
		valB4.setRefTs(cal.getTime());
		valBlist.add(valB4);
		b.setValues(valBlist);
		
		List<Point> points= new ArrayList<Point>();
		points.add(a);
		points.add(b);
		try {
			client.sendOnMessageAndResponse(points, "000TPO", new Date(), new Date(), "measure",1, 1, 1,Wssb2Client.MsgType.MEASURE);
			System.out.println("publish ok");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
