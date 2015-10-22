
/**
 * ExtensionMapper.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.6.2  Built on : Apr 17, 2012 (05:34:40 IST)
 */

        
            package com.fin_sif.sb.services;
        
            /**
            *  ExtensionMapper class
            */
            @SuppressWarnings({})
        
        public  class ExtensionMapper{

          public static java.lang.Object getTypeObject(java.lang.String namespaceURI,
                                                       java.lang.String typeName,
                                                       javax.xml.stream.XMLStreamReader reader) throws java.lang.Exception{

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "ComplexMsg".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.ComplexMsg.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "Subscription".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.Subscription.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "ModeType".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.ModeType.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "Filters".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.Filters.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "sysType".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.SysType.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "Filter".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.Filter.Factory.parse(reader);
                        

                  }

              
                  if (
                  "http://sb.fin-sif.com/types".equals(namespaceURI) &&
                  "onMessageType".equals(typeName)){
                   
                            return  com.fin_sif.sb.types.OnMessageType.Factory.parse(reader);
                        

                  }

              
             throw new org.apache.axis2.databinding.ADBException("Unsupported type " + namespaceURI + " " + typeName);
          }

        }
    