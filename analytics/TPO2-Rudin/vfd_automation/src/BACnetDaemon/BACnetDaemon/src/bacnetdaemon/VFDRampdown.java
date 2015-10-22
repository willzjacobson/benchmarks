package bacnetdaemon;

import java.util.List;
import java.util.Map;
import java.util.logging.*;
import java.util.Date;
import java.text.SimpleDateFormat;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
 

import com.serotonin.bacnet4j.event.DeviceEventAdapter;
import com.serotonin.bacnet4j.event.DeviceEventListener;
import com.serotonin.bacnet4j.exception.BACnetException;
import com.serotonin.bacnet4j.LocalDevice;
import com.serotonin.bacnet4j.npdu.ip.InetAddrCache;
import com.serotonin.bacnet4j.npdu.ip.IpNetwork;
import com.serotonin.bacnet4j.obj.BACnetObject;
import com.serotonin.bacnet4j.RemoteDevice;
import com.serotonin.bacnet4j.RemoteObject;
import com.serotonin.bacnet4j.service.acknowledgement.ReadPropertyAck;
import com.serotonin.bacnet4j.service.confirmed.ReadPropertyRequest;
import com.serotonin.bacnet4j.service.confirmed.ReinitializeDeviceRequest.ReinitializedStateOfDevice;
import com.serotonin.bacnet4j.service.confirmed.WritePropertyRequest;
import com.serotonin.bacnet4j.service.unconfirmed.WhoIsRequest;
import com.serotonin.bacnet4j.transport.Transport;
import com.serotonin.bacnet4j.type.constructed.Address;
import com.serotonin.bacnet4j.type.constructed.Choice;
import com.serotonin.bacnet4j.type.constructed.DateTime;
import com.serotonin.bacnet4j.type.constructed.ObjectPropertyReference;
import com.serotonin.bacnet4j.type.constructed.PropertyValue;
import com.serotonin.bacnet4j.type.constructed.SequenceOf;
import com.serotonin.bacnet4j.type.constructed.ServicesSupported;
import com.serotonin.bacnet4j.type.constructed.TimeStamp;
import com.serotonin.bacnet4j.type.Encodable;
import com.serotonin.bacnet4j.type.enumerated.EventState;
import com.serotonin.bacnet4j.type.enumerated.EventType;
import com.serotonin.bacnet4j.type.enumerated.MessagePriority;
import com.serotonin.bacnet4j.type.enumerated.NotifyType;
import com.serotonin.bacnet4j.type.enumerated.PropertyIdentifier;
import com.serotonin.bacnet4j.type.enumerated.Segmentation;
import com.serotonin.bacnet4j.type.notificationParameters.NotificationParameters;
import com.serotonin.bacnet4j.type.primitive.Boolean;
import com.serotonin.bacnet4j.type.primitive.CharacterString;
import com.serotonin.bacnet4j.type.primitive.ObjectIdentifier;
import com.serotonin.bacnet4j.type.primitive.OctetString;
import com.serotonin.bacnet4j.type.primitive.Unsigned16;
import com.serotonin.bacnet4j.type.primitive.UnsignedInteger;
import com.serotonin.bacnet4j.type.primitive.Enumerated;
import com.serotonin.bacnet4j.util.PropertyReferences;
import com.serotonin.bacnet4j.util.PropertyValues;
import com.serotonin.bacnet4j.util.RequestUtils;


public class VFDRampdown {
    static LocalDevice localDevice;
    private static RemoteDevice d;
    private static RemoteDevice remoteDevice;
    private static RemoteObject o;
    private static RemoteObject remoteObject;

    public static void main(String[] args) throws Exception {
        
        
      // get the command from the XML file
      String TStamp = "";
      String Action = "0";
      boolean newAction = false; 
      int ac = 0;
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

                           TStamp = eElement.getElementsByTagName("timestamp").item(0).getTextContent();
                           Action = eElement.getElementsByTagName("action").item(0).getTextContent();
                           
                           Action = eElement.getElementsByTagName("action").item(0).getTextContent();
                           System.out.println("timestamp : " + eElement.getElementsByTagName("timestamp").item(0).getTextContent());
                           System.out.println("action : " + eElement.getElementsByTagName("action").item(0).getTextContent());

                   }
           //}
       } catch (Exception e) {
           e.printStackTrace();
       }
        
        Date dateNow = new Date();
        String s = TStamp;
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

            if (diffInSeconds <= 1200){
                newAction = true;
                ac = Integer.parseInt(Action);
            }
            System.out.println("dateNow : "+dateNow.toString());
            System.out.println("TimeStamp : "+d.toString());
            System.out.println("diffInSeconds : "+diffInSeconds);
        }
        catch (Exception ex)
        {
            System.out.println("Exception "+ex);
        }

        
        
        IpNetwork network = new IpNetwork();
        Transport transport = new Transport(network);
        int instanceId = 4138819;
        String timeStamp = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date());

        //        transport.setTimeout(15000);
        //        transport.setSegTimeout(15000);
        localDevice = new LocalDevice(1234, transport);
        try {
            localDevice.initialize();
            localDevice.getEventHandler().addListener(new Listener());
            localDevice.sendGlobalBroadcast(new WhoIsRequest());
            
            Thread.sleep(5000);
            
            remoteDevice = localDevice.getRemoteDevice(instanceId);
            

            getExtendedDeviceInformation(remoteDevice);
            //System.out.println("Done getting extended information");

            List oids = ((SequenceOf) RequestUtils.sendReadPropertyAllowNull(localDevice, remoteDevice, remoteDevice.getObjectIdentifier(), PropertyIdentifier.objectList)).getValues();
            System.out.println(oids);
            
            Map<PropertyIdentifier, Encodable> values = RequestUtils.getProperties(localDevice, remoteDevice, null,
                PropertyIdentifier.objectName, PropertyIdentifier.vendorName, PropertyIdentifier.modelName, PropertyIdentifier.objectIdentifier,  
                PropertyIdentifier.description, PropertyIdentifier.location, PropertyIdentifier.objectList, PropertyIdentifier.presentValue);
            System.out.println(values);

            
            RequestUtils.getExtendedDeviceInformation(localDevice, remoteDevice);
            List<ObjectIdentifier> oidss = ((SequenceOf<ObjectIdentifier>) RequestUtils.sendReadPropertyAllowNull(localDevice, remoteDevice, remoteDevice.getObjectIdentifier(), PropertyIdentifier.objectList)).getValues();

            PropertyReferences refs = new PropertyReferences();
            // add the property references of the "device object" to the list
            refs.add(remoteDevice.getObjectIdentifier(), PropertyIdentifier.all);

            // and now from all objects under the device object >> ai0, ai1,bi0,bi1...
            for (ObjectIdentifier oid : oidss) {
                refs.add(oid, PropertyIdentifier.all);
            }

            System.out.println("Start read properties");
            final long start = System.currentTimeMillis();

            PropertyValues pvs = RequestUtils.readProperties(localDevice, remoteDevice, refs, null);
            System.out.println(String.format("Properties read done in %d ms", System.currentTimeMillis() - start));
            printObject(remoteDevice.getObjectIdentifier(), pvs);
            
            
            
            
            //Encodable value = new com.serotonin.bacnet4j.type.primitive.Boolean(true);
            
            Encodable value = new com.serotonin.bacnet4j.type.enumerated.BinaryPV(ac);
            
            String result = "PRESENT VALUE NOT CHANGED BY VFDRampdown";
            
            if (newAction){
            
                for (ObjectIdentifier oid : oidss) {
                    printObject(oid, pvs);

                    if (oid.getInstanceNumber()==7015){
                        WritePropertyRequest wpr = new WritePropertyRequest(oid, PropertyIdentifier.presentValue, null, value, new UnsignedInteger(10));
                        localDevice.send(remoteDevice, wpr);
                        System.out.println("***PRESENT VALUE SET TO "+ Action + " FOR: " + oid.getInstanceNumber() + " ***");
                        result = "PRESENT VALUE SET TO "+ Action + " FOR: " + oid.getInstanceNumber();
                    }

                }

                Logger logger = Logger.getLogger("MyLog");  
                FileHandler fh;  

                try {  

                    // This block configure the logger with handler and formatter  
                    fh = new FileHandler("D:/BACnet/Daemon/VFD_Logs_" + timeStamp.toString() + ".log");  
                    logger.addHandler(fh);
                    SimpleFormatter formatter = new SimpleFormatter();  
                    fh.setFormatter(formatter);  

                    // the following statement is used to log any messages  
                    logger.info(result);  

                } catch (SecurityException e) {  
                    e.printStackTrace();  
                }
            
            }
           
            /*for (ObjectIdentifier oid : oids) {
                
                System.out.println(remoteDevice.getObject(oid).toString());
                
            }*/

            /*
            localDevice.readProperties(d, refs);
            System.out.println("Values of d: " + d);
            try {
                // Send the read request.
                PropertyValues values = localDevice.readProperties(d, refs);

                // Dereference the property values back into the points.
                for (ObjectIdentifier oid : oids) {
                    printObject(oid, refs, values);
                }
            } catch (BACnetException e) {
                System.out.println("event.bacnet.readDevice ADDRESS: " + e.getMessage());
            }*/
            /*
            String objectid = "Binary Value 7015";
            for (RemoteObject o : remoteDevice.getObjects()) {
                System.out.println("Object name: " + o.getObjectName().toString());
                System.out.println("Object identifier: " + o.getObjectIdentifier().toString());
                
                if (o.getObjectIdentifier().equals(objectid)) {
                    remoteObject = o;
                    WritePropertyRequest wpr = new WritePropertyRequest(remoteObject.getObjectIdentifier(), PropertyIdentifier.presentValue, null, null, new UnsignedInteger(1));
                    localDevice.send(remoteDevice, wpr);
                    System.out.println("Value has been set");
                    break;
                }
            }
            * */
            //System.out.println("Properties");
            //System.out.println(RequestUtils.getProperty(localDevice, remoteDevice, remoteDevice.getObjectIdentifier(), PropertyIdentifier.priority).toString());
            //for (RemoteObject o : remoteDevice.getObjects()) {
                //getPresentValue();
                //getPriorityArray();
            //}

            
        } 
        catch (BACnetException e) {
             e.printStackTrace();
        } 
        catch (Exception e) {
             e.printStackTrace();
        }
        finally {
            localDevice.terminate();
        }
    }

    static class Listener extends DeviceEventAdapter {
        @Override
        public void iAmReceived(RemoteDevice d) {
            //try {
            
                if (d.getInstanceNumber()== 4138819){
                
                    System.out.println("IAm received from " + d);
                    System.out.println("Segmentation: " + d.getSegmentationSupported());
                    d.setSegmentationSupported(Segmentation.noSegmentation);

                    Address a = new Address(new Unsigned16(0), new OctetString(new byte[] { (byte) 0xc0, (byte) 0xa8, 0x1,
                            0x5, (byte) 0xba, (byte) 0xc0 }));

                    System.out.println("Equals: " + a.equals(d.getAddress()));
                    System.out.println("Name: " + d.getName());
                    System.out.println("Address: " + d.getAddress().toString());
                    System.out.println("InstanceNumber: " + d.getInstanceNumber());
                    System.out.println("DeviceObjectIdentifier: " + d.getObjectIdentifier());
                    System.out.println("RemoteObjects: " + d.getObjects().toString());
                    //for (RemoteObject o : d.getObjects()) {

                        //System.out.println("ObjectIdentifier: " + o.getObjectIdentifier());
                        //System.out.println("ObjectName: " + o.getObjectName());
                        //try {
                            //getPresentValue();
                        //} catch (Exception e) {
                            //e.printStackTrace();
                        //}
                    //if (o.getObjectIdentifier().equals(objectId)) {
                      //  remoteObject = o;
                      //  break;
                    //}

                    //}
                   // getExtendedDeviceInformation(d);
                   // System.out.println("Done getting extended information");

                   // List oids = ((SequenceOf) RequestUtils.sendReadPropertyAllowNull(localDevice, d,
                    //        d.getObjectIdentifier(), PropertyIdentifier.objectList)).getValues();
                
                
                    //System.out.println(oids);
                }
            //}
            //catch (BACnetException e) {
              //  e.printStackTrace();
            //}
        }
    }
    
    private static void printObject(ObjectIdentifier oid, PropertyValues pvs) {
        System.out.println(String.format("\t%s", oid));
        for (ObjectPropertyReference opr : pvs) {
            if (oid.equals(opr.getObjectIdentifier())) {
                System.out.println(String.format("\t\t%s = %s", opr.getPropertyIdentifier().toString(),
                        pvs.getNoErrorCheck(opr)));
            }

        }
    }
    private static void getPresentName() throws Exception {
        ReadPropertyRequest rpr = new ReadPropertyRequest(o.getObjectIdentifier(), PropertyIdentifier.objectName);
        ReadPropertyAck ack = (ReadPropertyAck) localDevice.send(remoteDevice, rpr);
        System.out.println("Present name: " + ack.getValue().toString());
    }
    
    private static void getPresentValue() throws Exception {
        ReadPropertyRequest rpr = new ReadPropertyRequest(o.getObjectIdentifier(), PropertyIdentifier.presentValue);
        ReadPropertyAck ack = (ReadPropertyAck) localDevice.send(remoteDevice, rpr);
        System.out.println("Present value: " + ack.getValue().toString());
    }
    
    private static void getPriorityArray() throws Exception {
        ReadPropertyRequest rpr = new ReadPropertyRequest(o.getObjectIdentifier(), PropertyIdentifier.priorityArray);
        ReadPropertyAck ack = (ReadPropertyAck) localDevice.send(remoteDevice, rpr);
        System.out.println("Priority array: " + ack.getValue().toString());
    }
        
    private static void setPresentValue(Encodable value, int priority) throws Exception {
        WritePropertyRequest wpr = new WritePropertyRequest(o.getObjectIdentifier(), PropertyIdentifier.presentValue, null, value, new UnsignedInteger(priority));
        localDevice.send(remoteDevice, wpr);
    }

    static void getExtendedDeviceInformation(RemoteDevice d) throws BACnetException {
        ObjectIdentifier oid = d.getObjectIdentifier();

        // Get the device's supported services
        //System.out.println("protocolServicesSupported");
        ReadPropertyAck ack = (ReadPropertyAck) localDevice.send(d, new ReadPropertyRequest(oid, PropertyIdentifier.protocolServicesSupported));
        d.setServicesSupported((ServicesSupported) ack.getValue());

        //System.out.println("objectName");
        ack = (ReadPropertyAck) localDevice.send(d, new ReadPropertyRequest(oid, PropertyIdentifier.objectName));
        d.setName(ack.getValue().toString());

        //System.out.println("protocolVersion");
        ack = (ReadPropertyAck) localDevice.send(d, new ReadPropertyRequest(oid, PropertyIdentifier.protocolVersion));
        d.setProtocolVersion((UnsignedInteger) ack.getValue());

        //        System.out.println("protocolRevision");
        //        ack = (ReadPropertyAck) localDevice.send(d, new ReadPropertyRequest(oid, PropertyIdentifier.protocolRevision));
        //        d.setProtocolRevision((UnsignedInteger) ack.getValue());
    }
}
