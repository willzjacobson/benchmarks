package spms.run.rudin.xmltool;

import java.util.Date;

public class Value {
	private boolean isNumber;
	
	private boolean isText;
	
	private boolean isBoolean;
	
	private Boolean value_Bool;
	
	private String value_Tx;
	
	private Double value_No;
	
	private Date refTs;
	
	public boolean isNumber() {
		return isNumber;
	}
	
	public boolean isText() {
		return isText;
	}
	
	public boolean isBoolean() {
		return isBoolean;
	}
	
	public Boolean getValue_Bool() {
		return value_Bool;
	}
	
	public void setValue_Bool(Boolean value_Bool) {
		this.isBoolean = true;
		this.value_Bool = value_Bool;
		this.isText = false;
		this.value_Tx = null;
		this.isNumber = false;
		this.value_No = null;
	}
	
	public String getValue_Tx() {
		return value_Tx;
	}
	
	public void setValue_Tx(String value_Tx) {
		this.isText = true;
		this.value_Tx = value_Tx;
		this.isBoolean = false;
		this.value_Bool = null;
		this.isNumber = false;
		this.value_No = null;
	}
	
	public Double getValue_No() {
		return value_No;
	}
	
	public void setValue_No(Double value_No) {
		this.isNumber = true;
		this.value_No = value_No;
		this.isBoolean = false;
		this.value_Bool = null;
		this.isText = false;
		this.value_Tx = null;
	}
	
	public Date getRefTs() {
		return refTs;
	}
	
	public void setRefTs(Date refTs) {
		this.refTs = refTs;
	}
	
	

}
