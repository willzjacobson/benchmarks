package communicator;

/**
 * This class represents a subscription that TPO-COM can make to SIF.
 * 
 * @author vivek
 * 
 */
public class InternalSubscription {
	/**
	 * public constructor for Sucscription class
	 * 
	 * @param type
	 *            type of the point - "measure" or "status"
	 * @param name
	 *            subscription name that SIF uses - "measure.>" or "status.>"
	 * @param filter
	 *            filter to avoid loop back messages - "measure/sender" or
	 *            "status/sender"
	 */
	public InternalSubscription(String type, String name, String filter) {
		this.type = type;
		this.name = name;
		this.filter = filter;
	}

	/**
	 * Returns the subscription name.
	 * 
	 * @return
	 */
	public String getName() {
		return this.name;
	}

	/**
	 * Returns the subscription point type.
	 * 
	 * @return
	 */
	public String getType() {
		return this.type;
	}

	/**
	 * Returns a filter that are to be applied along with this
	 * subscription
	 * 
	 * @return
	 */
	public String getFilter() {
		return this.filter;
	}

	private String type;
	private String name;
	private String filter;
}
