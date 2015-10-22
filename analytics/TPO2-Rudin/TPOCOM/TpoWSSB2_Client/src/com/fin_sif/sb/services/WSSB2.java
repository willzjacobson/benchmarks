

/**
 * WSSB2.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.6.2  Built on : Apr 17, 2012 (05:33:49 IST)
 */

    package com.fin_sif.sb.services;

    /*
     *  WSSB2 java interface
     */

    public interface WSSB2 {
          

        /**
          * Auto generated method signature
          * 
                    * @param sBUnRegister4
                
         */

         
                     public com.fin_sif.sb.types.SBResponse sBunregister(

                        com.fin_sif.sb.types.SBUnRegister sBUnRegister4)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sBUnRegister4
            
          */
        public void startsBunregister(

            com.fin_sif.sb.types.SBUnRegister sBUnRegister4,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param e2EonMessageAndResponse6
                
         */

         
                     public com.fin_sif.sb.types.OnMessageResponse e2EonMessageAndResponse(

                        com.fin_sif.sb.types.E2EonMessageAndResponse e2EonMessageAndResponse6)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param e2EonMessageAndResponse6
            
          */
        public void starte2EonMessageAndResponse(

            com.fin_sif.sb.types.E2EonMessageAndResponse e2EonMessageAndResponse6,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param sBSystemsList8
                
         */

         
                     public com.fin_sif.sb.types.SBSystemsListResp sBsystemslist(

                        com.fin_sif.sb.types.SBSystemsList sBSystemsList8)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sBSystemsList8
            
          */
        public void startsBsystemslist(

            com.fin_sif.sb.types.SBSystemsList sBSystemsList8,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param sBKeepAlive10
                
         */

         
                     public com.fin_sif.sb.types.SBResponse sBkeepalive(

                        com.fin_sif.sb.types.SBKeepAlive sBKeepAlive10)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sBKeepAlive10
            
          */
        public void startsBkeepalive(

            com.fin_sif.sb.types.SBKeepAlive sBKeepAlive10,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param onMessageAndResponse12
                
         */

         
                     public com.fin_sif.sb.types.OnMessageResponse onMessageAndResponse(

                        com.fin_sif.sb.types.OnMessageAndResponse onMessageAndResponse12)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param onMessageAndResponse12
            
          */
        public void startonMessageAndResponse(

            com.fin_sif.sb.types.OnMessageAndResponse onMessageAndResponse12,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param sBHealthStatus14
                
         */

         
                     public com.fin_sif.sb.types.SBHealthStatusResp sBhealthstatus(

                        com.fin_sif.sb.types.SBHealthStatus sBHealthStatus14)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sBHealthStatus14
            
          */
        public void startsBhealthstatus(

            com.fin_sif.sb.types.SBHealthStatus sBHealthStatus14,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param aDSetHDBSubscriptions16
                
         */

         
                     public com.fin_sif.sb.types.SBResponse aMsetHDBsubscriptions(

                        com.fin_sif.sb.types.ADSetHDBSubscriptions aDSetHDBSubscriptions16)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param aDSetHDBSubscriptions16
            
          */
        public void startaMsetHDBsubscriptions(

            com.fin_sif.sb.types.ADSetHDBSubscriptions aDSetHDBSubscriptions16,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     
       /**
         * Auto generated method signature for Asynchronous Invocations
         * 
         */
        public void  onMessage(
         com.fin_sif.sb.types.OnMessage onMessage18

        ) throws java.rmi.RemoteException
        
        ;

        

        /**
          * Auto generated method signature
          * 
                    * @param sBRegisterAndSubscribe19
                
         */

         
                     public com.fin_sif.sb.types.SBResponse sBregisterandsubscribe(

                        com.fin_sif.sb.types.SBRegisterAndSubscribe sBRegisterAndSubscribe19)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sBRegisterAndSubscribe19
            
          */
        public void startsBregisterandsubscribe(

            com.fin_sif.sb.types.SBRegisterAndSubscribe sBRegisterAndSubscribe19,

            final com.fin_sif.sb.services.WSSB2CallbackHandler callback)

            throws java.rmi.RemoteException;

     

        
       //
       }
    