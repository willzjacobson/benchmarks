package tpocom.sender;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

/**
 * Data object is a class to store a single data type which is either a string,
 * double, boolean or Date. It has standard getters and setters for the same. In 
 * addition it also provides the methods to query the type of data contained in the
 * Object
 * 
 * @author vivek
 * 
 */
public class DataObject {
	/**
	 * Default Constructor.
	 */
	public DataObject() {
		reset();
	}
	
	/**
	 * Takes in the result set and extracts data from the give colName
	 * as per the give type and stores it. 
	 * @param rs
	 * @param colName
	 * @param type
	 * @throws SQLException
	 */
	public DataObject(ResultSet rs, String colName, String type)
			throws SQLException {
		reset();
		if (type.equals("double")) {
			setNumber(rs.getDouble(colName));
		} else if(type.equals("integer")){
			setInteger(rs.getInt(colName));
		} else if (type.equals("string")) {
			setText(rs.getString(colName));
		} else if (type.equals("boolean")) {
			setBool(rs.getBoolean(colName));
		} else if (type.equals("date")) {
			setDate(rs.getTimestamp(colName));
		}
		// set null values in case the last result was null.
		// this can be identified later in the code and skipped.
		if(rs.wasNull()){
			reset();
		}
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((bool == null) ? 0 : bool.hashCode());
		result = prime * result + ((date == null) ? 0 : date.hashCode());
		result = prime * result + ((integer == null) ? 0 : integer.hashCode());
		result = prime * result + ((number == null) ? 0 : number.hashCode());
		result = prime * result + ((text == null) ? 0 : text.hashCode());
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
		DataObject other = (DataObject) obj;
		if (bool == null) {
			if (other.bool != null)
				return false;
		} else if (!bool.equals(other.bool))
			return false;
		if (date == null) {
			if (other.date != null)
				return false;
		} else if (!date.equals(other.date))
			return false;
		if (integer == null) {
			if (other.integer != null)
				return false;
		} else if (!integer.equals(other.integer))
			return false;
		if (number == null) {
			if (other.number != null)
				return false;
		} else if (!number.equals(other.number))
			return false;
		if (text == null) {
			if (other.text != null)
				return false;
		} else if (!text.equals(other.text))
			return false;
		return true;
	}

	private void reset() {
		this.bool = null;
		this.date = null;
		this.number = null;
		this.integer = null;
		this.text = null;
		this.isBoolean = false;
		this.isDate = false;
		this.isNumber = false;
		this.isInteger = false;
		this.isText = false;
	}
	
	public boolean isEmpty() {
		return !(this.isBoolean || this.isDate 
				|| this.isNumber || this.isText || this.isInteger);
	}

	public Double getNumber() {
		return number;
	}

	public void setNumber(Double number) {
		reset();
		this.number = number;
		this.isNumber = true;
	}
	
	public Integer getInteger() {
		return integer;
	}
	
	public void setInteger(Integer integer){
		reset();
		this.integer = integer;
		this.isInteger = true;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		reset();
		this.text = text;
		this.isText = true;
	}

	public Boolean getBool() {
		return bool;
	}

	public void setBool(Boolean bool) {
		reset();
		this.bool = bool;
		this.isBoolean = true;
	}

	public Date getDate() {
		return date;
	}

	public void setDate(Date date) {
		reset();
		this.date = date;
		this.isDate = true;
	}

	public boolean isBoolean() {
		return isBoolean;
	}

	public boolean isString() {
		return isText;
	}

	public boolean isNumber() {
		return isNumber;
	}
	
	public boolean isInteger(){
		return isInteger;
	}

	public boolean isDate() {
		return isDate;
	}

	// data members ; one of these is valid at a given time
	private String text;
	private Double number;
	private Integer integer;
	private Boolean bool;
	private Date date;

	// boolean indicating which of the datatypes are present in the object
	private boolean isText;
	private boolean isNumber;
	private boolean isInteger;
	private boolean isBoolean;
	private boolean isDate;
}
