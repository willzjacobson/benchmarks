package tpo.adapter.server.impl;


import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import spms.run.rudin.xmltool.Point;
import spms.run.rudin.xmltool.XMLReader;

import tpocom.receiver.ConfigurationReader;
import tpocom.receiver.ConnectionManager;
import tpocom.receiver.MsgDispatcher;

import com.fin_sif.sb.services.WSSB2SkeletonInterface;
import com.fin_sif.sb.types.ADSetHDBSubscriptions;
import com.fin_sif.sb.types.ComplexMsg;
import com.fin_sif.sb.types.E2EonMessageAndResponse;
import com.fin_sif.sb.types.OnMessage;
import com.fin_sif.sb.types.OnMessageAndResponse;
import com.fin_sif.sb.types.OnMessageResponse;
import com.fin_sif.sb.types.SBHealthStatus;
import com.fin_sif.sb.types.SBHealthStatusResp;
import com.fin_sif.sb.types.SBKeepAlive;
import com.fin_sif.sb.types.SBRegisterAndSubscribe;
import com.fin_sif.sb.types.SBResponse;
import com.fin_sif.sb.types.SBSystemsList;
import com.fin_sif.sb.types.SBSystemsListResp;
import com.fin_sif.sb.types.SBUnRegister;


public class Wssb2Impl implements WSSB2SkeletonInterface {
	static private ConfigurationReader cfReader = new ConfigurationReader();
	static private ConnectionManager conMan = new ConnectionManager(cfReader.getDbMap());
	static private MsgDispatcher msgDisptcher = new MsgDispatcher(conMan, cfReader.getPointConfigList()); 
	
	@Override
	public SBResponse sBunregister(SBUnRegister sBUnRegister) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public OnMessageResponse e2EonMessageAndResponse(
			E2EonMessageAndResponse e2EonMessageAndResponse) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public SBSystemsListResp sBsystemslist(SBSystemsList sBSystemsList) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public SBResponse sBkeepalive(SBKeepAlive sBKeepAlive) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public OnMessageResponse onMessageAndResponse(
			OnMessageAndResponse onMessageAndResponse) {
		OnMessageResponse onMessageResponse = new OnMessageResponse();
		onMessageResponse.setErrcode(0);
		onMessageResponse.setErrdesc("");
			
		ComplexMsg complexMessages[] = onMessageAndResponse.getOnMessageAndResponse().getMsg();
		
		List<Point> pointList = new ArrayList<Point>();
		for (ComplexMsg complexMsg : complexMessages) {
			try {
				Point pt = XMLReader.parse(complexMsg.getString());
				pointList.add(pt);
			} catch (Exception e) {
				e.printStackTrace();
				onMessageResponse.setErrcode(-1);
				onMessageResponse.setErrdesc("Could not save the point\n");
				System.out.println("Cannot Parse Message\n"
						+ complexMsg.getString());
			}
		}
		try {
			Wssb2Impl.msgDisptcher.despatch(pointList);
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return onMessageResponse;
	}

	@Override
	public SBHealthStatusResp sBhealthstatus(SBHealthStatus sBHealthStatus) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public SBResponse aMsetHDBsubscriptions(
			ADSetHDBSubscriptions aDSetHDBSubscriptions) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void onMessage(OnMessage onMessage) {
		// TODO Auto-generated method stub

	}

	@Override
	public SBResponse sBregisterandsubscribe(
			SBRegisterAndSubscribe sBRegisterAndSubscribe) {
		// TODO Auto-generated method stub
		return null;
	}

}
