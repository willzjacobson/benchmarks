package spms.run.rudin.xmltool;

import java.util.Date;
import java.util.List;


public class Point {

	private String point_Type;
	
	private String realtime;
	
	private Boolean bad;
	
	private Date ts;

	private String pbs;

	private String pbs_Loc_A1;

	private String pbs_Loc_A2;

	private String pbs_Loc_A3;

	private String pbs_Loc_A4;

	private String pbs_Sys_T;

	private String pbs_Sys_S;

	private String pbs_Eq_L1;

	private String pbs_Eq_L2;

	private String pbs_Eq_L3;

	private String pbs_Eq_n;
	
	private String pbs_Native;
	
	private String sign_Prog;

	private String sign_Code;
	
	private Date refTs;

	private String mobile_Tid;

	private String mobile_Cb;

	private String mobile_Did;
	
	private String sender;

	private Integer alarm_State;

	private Integer alarm_Prio;

	private Date alarm_Init_Ts;

	private Date alarm_Ack_Ts;

	private Date alarm_Norm_Ts;
	
	private String lob_Pbs;
	
	private String lob_Sign;
	
	private Long samp;
	
	private List<Value> values;

	public String getPoint_Type() {
		return point_Type;
	}

	public void setPoint_Type(String point_Type) {
		this.point_Type = point_Type;
	}

	public String getRealtime() {
		return realtime;
	}

	public void setRealtime(String realtime) {
		this.realtime = realtime;
	}

	public Boolean isBad() {
		return bad;
	}

	public void setBad(Boolean bad) {
		this.bad = bad;
	}

	public Date getTs() {
		return ts;
	}

	public void setTs(Date ts) {
		this.ts = ts;
	}

	public String getPbs() {
		return pbs;
	}

	public void setPbs(String pbs) {
		this.pbs = pbs;
	}

	public String getPbs_Loc_A1() {
		return pbs_Loc_A1;
	}

	public void setPbs_Loc_A1(String pbs_Loc_A1) {
		this.pbs_Loc_A1 = pbs_Loc_A1;
	}

	public String getPbs_Loc_A2() {
		return pbs_Loc_A2;
	}

	public void setPbs_Loc_A2(String pbs_Loc_A2) {
		this.pbs_Loc_A2 = pbs_Loc_A2;
	}

	public String getPbs_Loc_A3() {
		return pbs_Loc_A3;
	}

	public void setPbs_Loc_A3(String pbs_Loc_A3) {
		this.pbs_Loc_A3 = pbs_Loc_A3;
	}

	public String getPbs_Loc_A4() {
		return pbs_Loc_A4;
	}

	public void setPbs_Loc_A4(String pbs_Loc_A4) {
		this.pbs_Loc_A4 = pbs_Loc_A4;
	}

	public String getPbs_Sys_T() {
		return pbs_Sys_T;
	}

	public void setPbs_Sys_T(String pbs_Sys_T) {
		this.pbs_Sys_T = pbs_Sys_T;
	}

	public String getPbs_Sys_S() {
		return pbs_Sys_S;
	}

	public void setPbs_Sys_S(String pbs_Sys_S) {
		this.pbs_Sys_S = pbs_Sys_S;
	}

	public String getPbs_Eq_L1() {
		return pbs_Eq_L1;
	}

	public void setPbs_Eq_L1(String pbs_Eq_L1) {
		this.pbs_Eq_L1 = pbs_Eq_L1;
	}

	public String getPbs_Eq_L2() {
		return pbs_Eq_L2;
	}

	public void setPbs_Eq_L2(String pbs_Eq_L2) {
		this.pbs_Eq_L2 = pbs_Eq_L2;
	}

	public String getPbs_Eq_L3() {
		return pbs_Eq_L3;
	}

	public void setPbs_Eq_L3(String pbs_Eq_L3) {
		this.pbs_Eq_L3 = pbs_Eq_L3;
	}

	public String getPbs_Eq_n() {
		return pbs_Eq_n;
	}

	public void setPbs_Eq_n(String pbs_Eq_n) {
		this.pbs_Eq_n = pbs_Eq_n;
	}

	public String getPbs_Native() {
		return pbs_Native;
	}

	public void setPbs_Native(String pbs_Native) {
		this.pbs_Native = pbs_Native;
	}

	public String getSign_Prog() {
		return sign_Prog;
	}

	public void setSign_Prog(String sign_Prog) {
		this.sign_Prog = sign_Prog;
	}

	public String getSign_Code() {
		return sign_Code;
	}

	public void setSign_Code(String sign_Code) {
		this.sign_Code = sign_Code;
	}

	public Date getRefTs() {
		return refTs;
	}

	public void setRefTs(Date refTs) {
		this.refTs = refTs;
	}

	public String getMobile_Tid() {
		return mobile_Tid;
	}

	public void setMobile_Tid(String mobile_Tid) {
		this.mobile_Tid = mobile_Tid;
	}

	public String getMobile_Cb() {
		return mobile_Cb;
	}

	public void setMobile_Cb(String mobile_Cb) {
		this.mobile_Cb = mobile_Cb;
	}

	public String getMobile_Did() {
		return mobile_Did;
	}

	public void setMobile_Did(String mobile_Did) {
		this.mobile_Did = mobile_Did;
	}

	public String getSender() {
		return sender;
	}

	public void setSender(String sender) {
		this.sender = sender;
	}

	public Integer getAlarm_State() {
		return alarm_State;
	}

	public void setAlarm_State(Integer alarm_State) {
		this.alarm_State = alarm_State;
	}

	public Integer getAlarm_Prio() {
		return alarm_Prio;
	}

	public void setAlarm_Prio(Integer alarm_Prio) {
		this.alarm_Prio = alarm_Prio;
	}

	public Date getAlarm_Init_Ts() {
		return alarm_Init_Ts;
	}

	public void setAlarm_Init_Ts(Date alarm_Init_Ts) {
		this.alarm_Init_Ts = alarm_Init_Ts;
	}

	public Date getAlarm_Ack_Ts() {
		return alarm_Ack_Ts;
	}

	public void setAlarm_Ack_Ts(Date alarm_Ack_Ts) {
		this.alarm_Ack_Ts = alarm_Ack_Ts;
	}

	public Date getAlarm_Norm_Ts() {
		return alarm_Norm_Ts;
	}

	public void setAlarm_Norm_Ts(Date alarm_Norm_Ts) {
		this.alarm_Norm_Ts = alarm_Norm_Ts;
	}

	public String getLob_Pbs() {
		return lob_Pbs;
	}

	public void setLob_Pbs(String lob_Pbs) {
		this.lob_Pbs = lob_Pbs;
	}

	public String getLob_Sign() {
		return lob_Sign;
	}

	public void setLob_Sign(String lob_Sign) {
		this.lob_Sign = lob_Sign;
	}

	public Long getSamp() {
		return samp;
	}

	public void setSamp(Long samp) {
		this.samp = samp;
	}

	public List<Value> getValues() {
		return values;
	}

	public void setValues(List<Value> values) {
		this.values = values;
	}

	@Override
	public String toString() {
		return "Point [point_Type=" + point_Type + ", realtime=" + realtime
				+ ", bad=" + bad + ", ts=" + ts + ", pbs=" + pbs
				+ ", pbs_Loc_A1=" + pbs_Loc_A1 + ", pbs_Loc_A2=" + pbs_Loc_A2
				+ ", pbs_Loc_A3=" + pbs_Loc_A3 + ", pbs_Loc_A4=" + pbs_Loc_A4
				+ ", pbs_Sys_T=" + pbs_Sys_T + ", pbs_Sys_S=" + pbs_Sys_S
				+ ", pbs_Eq_L1=" + pbs_Eq_L1 + ", pbs_Eq_L2=" + pbs_Eq_L2
				+ ", pbs_Eq_L3=" + pbs_Eq_L3 + ", pbs_Eq_n=" + pbs_Eq_n
				+ ", pbs_Native=" + pbs_Native + ", sign_Prog=" + sign_Prog
				+ ", sign_Code=" + sign_Code + ", refTs=" + refTs
				+ ", mobile_Tid=" + mobile_Tid + ", mobile_Cb=" + mobile_Cb
				+ ", mobile_Did=" + mobile_Did + ", sender=" + sender
				+ ", alarm_State=" + alarm_State + ", alarm_Prio=" + alarm_Prio
				+ ", alarm_Init_Ts=" + alarm_Init_Ts + ", alarm_Ack_Ts="
				+ alarm_Ack_Ts + ", alarm_Norm_Ts=" + alarm_Norm_Ts
				+ ", lob_Pbs=" + lob_Pbs + ", lob_Sign=" + lob_Sign + ", samp="
				+ samp + ", values=" + values + "]";
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result
				+ ((alarm_Ack_Ts == null) ? 0 : alarm_Ack_Ts.hashCode());
		result = prime * result
				+ ((alarm_Init_Ts == null) ? 0 : alarm_Init_Ts.hashCode());
		result = prime * result
				+ ((alarm_Norm_Ts == null) ? 0 : alarm_Norm_Ts.hashCode());
		result = prime * result
				+ ((alarm_Prio == null) ? 0 : alarm_Prio.hashCode());
		result = prime * result
				+ ((alarm_State == null) ? 0 : alarm_State.hashCode());
		result = prime * result + ((bad == null) ? 0 : bad.hashCode());
		result = prime * result + ((lob_Pbs == null) ? 0 : lob_Pbs.hashCode());
		result = prime * result
				+ ((lob_Sign == null) ? 0 : lob_Sign.hashCode());
		result = prime * result
				+ ((mobile_Cb == null) ? 0 : mobile_Cb.hashCode());
		result = prime * result
				+ ((mobile_Did == null) ? 0 : mobile_Did.hashCode());
		result = prime * result
				+ ((mobile_Tid == null) ? 0 : mobile_Tid.hashCode());
		result = prime * result + ((pbs == null) ? 0 : pbs.hashCode());
		result = prime * result
				+ ((pbs_Eq_L1 == null) ? 0 : pbs_Eq_L1.hashCode());
		result = prime * result
				+ ((pbs_Eq_L2 == null) ? 0 : pbs_Eq_L2.hashCode());
		result = prime * result
				+ ((pbs_Eq_L3 == null) ? 0 : pbs_Eq_L3.hashCode());
		result = prime * result
				+ ((pbs_Eq_n == null) ? 0 : pbs_Eq_n.hashCode());
		result = prime * result
				+ ((pbs_Loc_A1 == null) ? 0 : pbs_Loc_A1.hashCode());
		result = prime * result
				+ ((pbs_Loc_A2 == null) ? 0 : pbs_Loc_A2.hashCode());
		result = prime * result
				+ ((pbs_Loc_A3 == null) ? 0 : pbs_Loc_A3.hashCode());
		result = prime * result
				+ ((pbs_Loc_A4 == null) ? 0 : pbs_Loc_A4.hashCode());
		result = prime * result
				+ ((pbs_Native == null) ? 0 : pbs_Native.hashCode());
		result = prime * result
				+ ((pbs_Sys_S == null) ? 0 : pbs_Sys_S.hashCode());
		result = prime * result
				+ ((pbs_Sys_T == null) ? 0 : pbs_Sys_T.hashCode());
		result = prime * result
				+ ((point_Type == null) ? 0 : point_Type.hashCode());
		result = prime * result
				+ ((realtime == null) ? 0 : realtime.hashCode());
		result = prime * result + ((refTs == null) ? 0 : refTs.hashCode());
		result = prime * result + ((samp == null) ? 0 : samp.hashCode());
		result = prime * result + ((sender == null) ? 0 : sender.hashCode());
		result = prime * result
				+ ((sign_Code == null) ? 0 : sign_Code.hashCode());
		result = prime * result
				+ ((sign_Prog == null) ? 0 : sign_Prog.hashCode());
		result = prime * result + ((ts == null) ? 0 : ts.hashCode());
		result = prime * result + ((values == null) ? 0 : values.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Point other = (Point) obj;
		if (alarm_Ack_Ts == null) {
			if (other.alarm_Ack_Ts != null)
				return false;
		} else if (!alarm_Ack_Ts.equals(other.alarm_Ack_Ts))
			return false;
		if (alarm_Init_Ts == null) {
			if (other.alarm_Init_Ts != null)
				return false;
		} else if (!alarm_Init_Ts.equals(other.alarm_Init_Ts))
			return false;
		if (alarm_Norm_Ts == null) {
			if (other.alarm_Norm_Ts != null)
				return false;
		} else if (!alarm_Norm_Ts.equals(other.alarm_Norm_Ts))
			return false;
		if (alarm_Prio == null) {
			if (other.alarm_Prio != null)
				return false;
		} else if (!alarm_Prio.equals(other.alarm_Prio))
			return false;
		if (alarm_State == null) {
			if (other.alarm_State != null)
				return false;
		} else if (!alarm_State.equals(other.alarm_State))
			return false;
		if (bad == null) {
			if (other.bad != null)
				return false;
		} else if (!bad.equals(other.bad))
			return false;
		if (lob_Pbs == null) {
			if (other.lob_Pbs != null)
				return false;
		} else if (!lob_Pbs.equals(other.lob_Pbs))
			return false;
		if (lob_Sign == null) {
			if (other.lob_Sign != null)
				return false;
		} else if (!lob_Sign.equals(other.lob_Sign))
			return false;
		if (mobile_Cb == null) {
			if (other.mobile_Cb != null)
				return false;
		} else if (!mobile_Cb.equals(other.mobile_Cb))
			return false;
		if (mobile_Did == null) {
			if (other.mobile_Did != null)
				return false;
		} else if (!mobile_Did.equals(other.mobile_Did))
			return false;
		if (mobile_Tid == null) {
			if (other.mobile_Tid != null)
				return false;
		} else if (!mobile_Tid.equals(other.mobile_Tid))
			return false;
		if (pbs == null) {
			if (other.pbs != null)
				return false;
		} else if (!pbs.equals(other.pbs))
			return false;
		if (pbs_Eq_L1 == null) {
			if (other.pbs_Eq_L1 != null)
				return false;
		} else if (!pbs_Eq_L1.equals(other.pbs_Eq_L1))
			return false;
		if (pbs_Eq_L2 == null) {
			if (other.pbs_Eq_L2 != null)
				return false;
		} else if (!pbs_Eq_L2.equals(other.pbs_Eq_L2))
			return false;
		if (pbs_Eq_L3 == null) {
			if (other.pbs_Eq_L3 != null)
				return false;
		} else if (!pbs_Eq_L3.equals(other.pbs_Eq_L3))
			return false;
		if (pbs_Eq_n == null) {
			if (other.pbs_Eq_n != null)
				return false;
		} else if (!pbs_Eq_n.equals(other.pbs_Eq_n))
			return false;
		if (pbs_Loc_A1 == null) {
			if (other.pbs_Loc_A1 != null)
				return false;
		} else if (!pbs_Loc_A1.equals(other.pbs_Loc_A1))
			return false;
		if (pbs_Loc_A2 == null) {
			if (other.pbs_Loc_A2 != null)
				return false;
		} else if (!pbs_Loc_A2.equals(other.pbs_Loc_A2))
			return false;
		if (pbs_Loc_A3 == null) {
			if (other.pbs_Loc_A3 != null)
				return false;
		} else if (!pbs_Loc_A3.equals(other.pbs_Loc_A3))
			return false;
		if (pbs_Loc_A4 == null) {
			if (other.pbs_Loc_A4 != null)
				return false;
		} else if (!pbs_Loc_A4.equals(other.pbs_Loc_A4))
			return false;
		if (pbs_Native == null) {
			if (other.pbs_Native != null)
				return false;
		} else if (!pbs_Native.equals(other.pbs_Native))
			return false;
		if (pbs_Sys_S == null) {
			if (other.pbs_Sys_S != null)
				return false;
		} else if (!pbs_Sys_S.equals(other.pbs_Sys_S))
			return false;
		if (pbs_Sys_T == null) {
			if (other.pbs_Sys_T != null)
				return false;
		} else if (!pbs_Sys_T.equals(other.pbs_Sys_T))
			return false;
		if (point_Type == null) {
			if (other.point_Type != null)
				return false;
		} else if (!point_Type.equals(other.point_Type))
			return false;
		if (realtime == null) {
			if (other.realtime != null)
				return false;
		} else if (!realtime.equals(other.realtime))
			return false;
		if (refTs == null) {
			if (other.refTs != null)
				return false;
		} else if (!refTs.equals(other.refTs))
			return false;
		if (samp == null) {
			if (other.samp != null)
				return false;
		} else if (!samp.equals(other.samp))
			return false;
		if (sender == null) {
			if (other.sender != null)
				return false;
		} else if (!sender.equals(other.sender))
			return false;
		if (sign_Code == null) {
			if (other.sign_Code != null)
				return false;
		} else if (!sign_Code.equals(other.sign_Code))
			return false;
		if (sign_Prog == null) {
			if (other.sign_Prog != null)
				return false;
		} else if (!sign_Prog.equals(other.sign_Prog))
			return false;
		if (ts == null) {
			if (other.ts != null)
				return false;
		} else if (!ts.equals(other.ts))
			return false;
		if (values == null) {
			if (other.values != null)
				return false;
		} else if (!values.equals(other.values))
			return false;
		return true;
	}
	
}
