
/**
 * WSSB2CallbackHandler.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.6.2  Built on : Apr 17, 2012 (05:33:49 IST)
 */

    package com.fin_sif.sb.services;

    /**
     *  WSSB2CallbackHandler Callback class, Users can extend this class and implement
     *  their own receiveResult and receiveError methods.
     */
    public abstract class WSSB2CallbackHandler{



    protected Object clientData;

    /**
    * User can pass in any object that needs to be accessed once the NonBlocking
    * Web service call is finished and appropriate method of this CallBack is called.
    * @param clientData Object mechanism by which the user can pass in user data
    * that will be avilable at the time this callback is called.
    */
    public WSSB2CallbackHandler(Object clientData){
        this.clientData = clientData;
    }

    /**
    * Please use this constructor if you don't want to set any clientData
    */
    public WSSB2CallbackHandler(){
        this.clientData = null;
    }

    /**
     * Get the client data
     */

     public Object getClientData() {
        return clientData;
     }

        
           /**
            * auto generated Axis2 call back method for sBunregister method
            * override this method for handling normal response from sBunregister operation
            */
           public void receiveResultsBunregister(
                    com.fin_sif.sb.types.SBResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sBunregister operation
           */
            public void receiveErrorsBunregister(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for e2EonMessageAndResponse method
            * override this method for handling normal response from e2EonMessageAndResponse operation
            */
           public void receiveResulte2EonMessageAndResponse(
                    com.fin_sif.sb.types.OnMessageResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from e2EonMessageAndResponse operation
           */
            public void receiveErrore2EonMessageAndResponse(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for sBsystemslist method
            * override this method for handling normal response from sBsystemslist operation
            */
           public void receiveResultsBsystemslist(
                    com.fin_sif.sb.types.SBSystemsListResp result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sBsystemslist operation
           */
            public void receiveErrorsBsystemslist(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for sBkeepalive method
            * override this method for handling normal response from sBkeepalive operation
            */
           public void receiveResultsBkeepalive(
                    com.fin_sif.sb.types.SBResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sBkeepalive operation
           */
            public void receiveErrorsBkeepalive(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for onMessageAndResponse method
            * override this method for handling normal response from onMessageAndResponse operation
            */
           public void receiveResultonMessageAndResponse(
                    com.fin_sif.sb.types.OnMessageResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from onMessageAndResponse operation
           */
            public void receiveErroronMessageAndResponse(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for sBhealthstatus method
            * override this method for handling normal response from sBhealthstatus operation
            */
           public void receiveResultsBhealthstatus(
                    com.fin_sif.sb.types.SBHealthStatusResp result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sBhealthstatus operation
           */
            public void receiveErrorsBhealthstatus(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for aMsetHDBsubscriptions method
            * override this method for handling normal response from aMsetHDBsubscriptions operation
            */
           public void receiveResultaMsetHDBsubscriptions(
                    com.fin_sif.sb.types.SBResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from aMsetHDBsubscriptions operation
           */
            public void receiveErroraMsetHDBsubscriptions(java.lang.Exception e) {
            }
                
               // No methods generated for meps other than in-out
                
           /**
            * auto generated Axis2 call back method for sBregisterandsubscribe method
            * override this method for handling normal response from sBregisterandsubscribe operation
            */
           public void receiveResultsBregisterandsubscribe(
                    com.fin_sif.sb.types.SBResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sBregisterandsubscribe operation
           */
            public void receiveErrorsBregisterandsubscribe(java.lang.Exception e) {
            }
                


    }
    