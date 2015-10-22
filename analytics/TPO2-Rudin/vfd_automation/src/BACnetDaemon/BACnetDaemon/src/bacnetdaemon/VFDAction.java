/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package bacnetdaemon;


import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.TimeUnit;
 
public class VFDAction {
 
  public static void main(String argv[]) {
      
    String TimeStamp = "";
    String Action = "";
    boolean newAction = false; 
    
    try {
 
	File fXmlFile = new File("D:\\BACnet\\XML\\VFD_Actions.XML");
	DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
	Document doc = dBuilder.parse(fXmlFile);
 
	//optional, but recommended
	//read this - http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
	doc.getDocumentElement().normalize();
 
	//System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
 
	NodeList nList = doc.getElementsByTagName("_x0033_45.dbo.occupancy_vfd_triggers");
 
	//System.out.println("----------------------------");
 
	//for (int temp = 0; temp < nList.getLength(); temp++) {
 
                int temp = 0; 
		Node nNode = nList.item(temp);
 
		//System.out.println("\nCurrent Element :" + nNode.getNodeName());
 
		if (nNode.getNodeType() == Node.ELEMENT_NODE) {
 
			Element eElement = (Element) nNode;
 
                        TimeStamp = eElement.getElementsByTagName("timestamp").item(0).getTextContent();
                        Action = eElement.getElementsByTagName("action").item(0).getTextContent();
                           
			System.out.println("timestamp : " + eElement.getElementsByTagName("timestamp").item(0).getTextContent());
			System.out.println("action : " + eElement.getElementsByTagName("action").item(0).getTextContent());

		}
	//}
    } catch (Exception e) {
	e.printStackTrace();
    }
    
    Date dateNow = new Date();
    String s = TimeStamp;
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
    try
    {
        Date d = simpleDateFormat.parse(s);
        long duration =  dateNow.getTime() - d.getTime();
        long diffInSeconds = duration / 1000;
        //long diffInSeconds = duration / 1000 % 60;
        //long diffInSeconds = TimeUnit.MILLISECONDS.toSeconds(duration);
        //long diffInMinutes = TimeUnit.MILLISECONDS.toMinutes(duration);
        //long diffInHours = TimeUnit.MILLISECONDS.toHours(duration);
        
        if (diffInSeconds < 300){
            newAction = true;
        }
        System.out.println("dateNow : "+dateNow.toString());
        System.out.println("TimeStamp : "+d.toString());
        System.out.println("diffInSeconds : "+diffInSeconds);
    }
    catch (Exception ex)
    {
        System.out.println("Exception "+ex);
    }
  
    
  }
 
}