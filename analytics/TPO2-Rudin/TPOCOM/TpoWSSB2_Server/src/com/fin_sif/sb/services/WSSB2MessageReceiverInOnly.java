

/**
 * WSSB2MessageReceiverInOnly.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.6.2  Built on : Apr 17, 2012 (05:33:49 IST)
 */
        package com.fin_sif.sb.services;

        /**
        *  WSSB2MessageReceiverInOnly message receiver
        */

        public class WSSB2MessageReceiverInOnly extends org.apache.axis2.receivers.AbstractInMessageReceiver{

        public void invokeBusinessLogic(org.apache.axis2.context.MessageContext inMessage) throws org.apache.axis2.AxisFault{

        try {

        // get the implementation class for the Web Service
        Object obj = getTheImplementationObject(inMessage);

        WSSB2SkeletonInterface skel = (WSSB2SkeletonInterface)obj;
        //Find the axisOperation that has been set by the Dispatch phase.
        org.apache.axis2.description.AxisOperation op = inMessage.getOperationContext().getAxisOperation();
        if (op == null) {
        throw new org.apache.axis2.AxisFault("Operation is not located, if this is doclit style the SOAP-ACTION should specified via the SOAP Action to use the RawXMLProvider");
        }

        java.lang.String methodName;
        if((op.getName() != null) && ((methodName = org.apache.axis2.util.JavaUtils.xmlNameToJavaIdentifier(op.getName().getLocalPart())) != null)){

        
            if("onMessage".equals(methodName)){
            
            com.fin_sif.sb.types.OnMessage wrappedParam = (com.fin_sif.sb.types.OnMessage)fromOM(
                                                        inMessage.getEnvelope().getBody().getFirstElement(),
                                                        com.fin_sif.sb.types.OnMessage.class,
                                                        getEnvelopeNamespaces(inMessage.getEnvelope()));
                                            
                                                     skel.onMessage(wrappedParam);
                                                
                } else {
                  throw new java.lang.RuntimeException("method not found");
                }
            

        }
        } catch (java.lang.Exception e) {
        throw org.apache.axis2.AxisFault.makeFault(e);
        }
        }


        
        //
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBUnRegister param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBUnRegister.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBResponse param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBResponse.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.E2EonMessageAndResponse param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.E2EonMessageAndResponse.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.OnMessageResponse param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.OnMessageResponse.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBSystemsList param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBSystemsList.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBSystemsListResp param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBSystemsListResp.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBKeepAlive param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBKeepAlive.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.OnMessageAndResponse param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.OnMessageAndResponse.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBHealthStatus param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBHealthStatus.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBHealthStatusResp param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBHealthStatusResp.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.ADSetHDBSubscriptions param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.ADSetHDBSubscriptions.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.OnMessage param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.OnMessage.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
            @SuppressWarnings("unused")
			private  org.apache.axiom.om.OMElement  toOM(com.fin_sif.sb.types.SBRegisterAndSubscribe param, boolean optimizeContent)
            throws org.apache.axis2.AxisFault {

            
                        try{
                             return param.getOMElement(com.fin_sif.sb.types.SBRegisterAndSubscribe.MY_QNAME,
                                          org.apache.axiom.om.OMAbstractFactory.getOMFactory());
                        } catch(org.apache.axis2.databinding.ADBException e){
                            throw org.apache.axis2.AxisFault.makeFault(e);
                        }
                    

            }
        
                    @SuppressWarnings("unused")
					private  org.apache.axiom.soap.SOAPEnvelope toEnvelope(org.apache.axiom.soap.SOAPFactory factory, com.fin_sif.sb.types.SBResponse param, boolean optimizeContent, javax.xml.namespace.QName methodQName)
                        throws org.apache.axis2.AxisFault{
                      try{
                          org.apache.axiom.soap.SOAPEnvelope emptyEnvelope = factory.getDefaultEnvelope();
                           
                                    emptyEnvelope.getBody().addChild(param.getOMElement(com.fin_sif.sb.types.SBResponse.MY_QNAME,factory));
                                

                         return emptyEnvelope;
                    } catch(org.apache.axis2.databinding.ADBException e){
                        throw org.apache.axis2.AxisFault.makeFault(e);
                    }
                    }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBResponse wrapSBunregister(){
                                com.fin_sif.sb.types.SBResponse wrappedElement = new com.fin_sif.sb.types.SBResponse();
                                return wrappedElement;
                         }
                    
                    @SuppressWarnings("unused")
					private  org.apache.axiom.soap.SOAPEnvelope toEnvelope(org.apache.axiom.soap.SOAPFactory factory, com.fin_sif.sb.types.OnMessageResponse param, boolean optimizeContent, javax.xml.namespace.QName methodQName)
                        throws org.apache.axis2.AxisFault{
                      try{
                          org.apache.axiom.soap.SOAPEnvelope emptyEnvelope = factory.getDefaultEnvelope();
                           
                                    emptyEnvelope.getBody().addChild(param.getOMElement(com.fin_sif.sb.types.OnMessageResponse.MY_QNAME,factory));
                                

                         return emptyEnvelope;
                    } catch(org.apache.axis2.databinding.ADBException e){
                        throw org.apache.axis2.AxisFault.makeFault(e);
                    }
                    }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.OnMessageResponse wrape2EonMessageAndResponse(){
                                com.fin_sif.sb.types.OnMessageResponse wrappedElement = new com.fin_sif.sb.types.OnMessageResponse();
                                return wrappedElement;
                         }
                    
                    @SuppressWarnings("unused")
					private  org.apache.axiom.soap.SOAPEnvelope toEnvelope(org.apache.axiom.soap.SOAPFactory factory, com.fin_sif.sb.types.SBSystemsListResp param, boolean optimizeContent, javax.xml.namespace.QName methodQName)
                        throws org.apache.axis2.AxisFault{
                      try{
                          org.apache.axiom.soap.SOAPEnvelope emptyEnvelope = factory.getDefaultEnvelope();
                           
                                    emptyEnvelope.getBody().addChild(param.getOMElement(com.fin_sif.sb.types.SBSystemsListResp.MY_QNAME,factory));
                                

                         return emptyEnvelope;
                    } catch(org.apache.axis2.databinding.ADBException e){
                        throw org.apache.axis2.AxisFault.makeFault(e);
                    }
                    }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBSystemsListResp wrapSBsystemslist(){
                                com.fin_sif.sb.types.SBSystemsListResp wrappedElement = new com.fin_sif.sb.types.SBSystemsListResp();
                                return wrappedElement;
                         }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBResponse wrapSBkeepalive(){
                                com.fin_sif.sb.types.SBResponse wrappedElement = new com.fin_sif.sb.types.SBResponse();
                                return wrappedElement;
                         }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.OnMessageResponse wraponMessageAndResponse(){
                                com.fin_sif.sb.types.OnMessageResponse wrappedElement = new com.fin_sif.sb.types.OnMessageResponse();
                                return wrappedElement;
                         }
                    
                    @SuppressWarnings("unused")
					private  org.apache.axiom.soap.SOAPEnvelope toEnvelope(org.apache.axiom.soap.SOAPFactory factory, com.fin_sif.sb.types.SBHealthStatusResp param, boolean optimizeContent, javax.xml.namespace.QName methodQName)
                        throws org.apache.axis2.AxisFault{
                      try{
                          org.apache.axiom.soap.SOAPEnvelope emptyEnvelope = factory.getDefaultEnvelope();
                           
                                    emptyEnvelope.getBody().addChild(param.getOMElement(com.fin_sif.sb.types.SBHealthStatusResp.MY_QNAME,factory));
                                

                         return emptyEnvelope;
                    } catch(org.apache.axis2.databinding.ADBException e){
                        throw org.apache.axis2.AxisFault.makeFault(e);
                    }
                    }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBHealthStatusResp wrapSBhealthstatus(){
                                com.fin_sif.sb.types.SBHealthStatusResp wrappedElement = new com.fin_sif.sb.types.SBHealthStatusResp();
                                return wrappedElement;
                         }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBResponse wrapAMsetHDBsubscriptions(){
                                com.fin_sif.sb.types.SBResponse wrappedElement = new com.fin_sif.sb.types.SBResponse();
                                return wrappedElement;
                         }
                    
                         @SuppressWarnings("unused")
						private com.fin_sif.sb.types.SBResponse wrapSBregisterandsubscribe(){
                                com.fin_sif.sb.types.SBResponse wrappedElement = new com.fin_sif.sb.types.SBResponse();
                                return wrappedElement;
                         }
                    


        /**
        *  get the default envelope
        */
        @SuppressWarnings("unused")
		private org.apache.axiom.soap.SOAPEnvelope toEnvelope(org.apache.axiom.soap.SOAPFactory factory){
        return factory.getDefaultEnvelope();
        }


        @SuppressWarnings("rawtypes")
		private  java.lang.Object fromOM(
        org.apache.axiom.om.OMElement param,
        java.lang.Class type,
        java.util.Map extraNamespaces) throws org.apache.axis2.AxisFault{

        try {
        
                if (com.fin_sif.sb.types.SBUnRegister.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBUnRegister.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.E2EonMessageAndResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.E2EonMessageAndResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.OnMessageResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.OnMessageResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBSystemsList.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBSystemsList.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBSystemsListResp.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBSystemsListResp.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBKeepAlive.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBKeepAlive.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.OnMessageAndResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.OnMessageAndResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.OnMessageResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.OnMessageResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBHealthStatus.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBHealthStatus.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBHealthStatusResp.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBHealthStatusResp.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.ADSetHDBSubscriptions.class.equals(type)){
                
                           return com.fin_sif.sb.types.ADSetHDBSubscriptions.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.OnMessage.class.equals(type)){
                
                           return com.fin_sif.sb.types.OnMessage.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBRegisterAndSubscribe.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBRegisterAndSubscribe.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
                if (com.fin_sif.sb.types.SBResponse.class.equals(type)){
                
                           return com.fin_sif.sb.types.SBResponse.Factory.parse(param.getXMLStreamReaderWithoutCaching());
                    

                }
           
        } catch (java.lang.Exception e) {
        throw org.apache.axis2.AxisFault.makeFault(e);
        }
           return null;
        }



    



        /**
        *  A utility method that copies the namepaces from the SOAPEnvelope
        */
        @SuppressWarnings({ "rawtypes", "unchecked" })
		private java.util.Map getEnvelopeNamespaces(org.apache.axiom.soap.SOAPEnvelope env){
        java.util.Map returnMap = new java.util.HashMap();
        java.util.Iterator namespaceIterator = env.getAllDeclaredNamespaces();
        while (namespaceIterator.hasNext()) {
        org.apache.axiom.om.OMNamespace ns = (org.apache.axiom.om.OMNamespace) namespaceIterator.next();
        returnMap.put(ns.getPrefix(),ns.getNamespaceURI());
        }
        return returnMap;
        }



        }//end of class

    