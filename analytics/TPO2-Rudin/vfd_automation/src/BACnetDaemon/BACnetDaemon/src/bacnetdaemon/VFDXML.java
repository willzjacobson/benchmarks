/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package bacnetdaemon;

/**
 *
 * @author user
 */


import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;
import java.io.File;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;

public class VFDXML {
    public static void main (String[] args) throws IOException, ParserConfigurationException, SAXException, TransformerException {
        URL url = new URL("http://tpo.rudin.com/shared/VFD_Actions.XML");
        URLConnection conn = url.openConnection();

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(conn.getInputStream());

        TransformerFactory tfactory = TransformerFactory.newInstance();
        Transformer xform = tfactory.newTransformer();

        // that’s the default xform; use a stylesheet to get a real one
        //xform.transform(new DOMSource(doc), new StreamResult(System.out));
        File myOutput = new File("D:\\BACnet\\XML\\VFD_Actions.XML");
        xform.transform(new DOMSource(doc), new StreamResult(myOutput));
    }
}