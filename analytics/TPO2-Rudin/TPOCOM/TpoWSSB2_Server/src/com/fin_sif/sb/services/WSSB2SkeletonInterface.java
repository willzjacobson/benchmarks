
/**
 * WSSB2SkeletonInterface.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.6.2  Built on : Apr 17, 2012 (05:33:49 IST)
 */
    package com.fin_sif.sb.services;
    /**
     *  WSSB2SkeletonInterface java skeleton interface for the axisService
     */
    public interface WSSB2SkeletonInterface {
     
         
        /**
         * Auto generated method signature
         * 
                                    * @param sBUnRegister
         */

        
                public com.fin_sif.sb.types.SBResponse sBunregister
                (
                  com.fin_sif.sb.types.SBUnRegister sBUnRegister
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param e2EonMessageAndResponse
         */

        
                public com.fin_sif.sb.types.OnMessageResponse e2EonMessageAndResponse
                (
                  com.fin_sif.sb.types.E2EonMessageAndResponse e2EonMessageAndResponse
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param sBSystemsList
         */

        
                public com.fin_sif.sb.types.SBSystemsListResp sBsystemslist
                (
                  com.fin_sif.sb.types.SBSystemsList sBSystemsList
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param sBKeepAlive
         */

        
                public com.fin_sif.sb.types.SBResponse sBkeepalive
                (
                  com.fin_sif.sb.types.SBKeepAlive sBKeepAlive
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param onMessageAndResponse
         */

        
                public com.fin_sif.sb.types.OnMessageResponse onMessageAndResponse
                (
                  com.fin_sif.sb.types.OnMessageAndResponse onMessageAndResponse
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param sBHealthStatus
         */

        
                public com.fin_sif.sb.types.SBHealthStatusResp sBhealthstatus
                (
                  com.fin_sif.sb.types.SBHealthStatus sBHealthStatus
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param aDSetHDBSubscriptions
         */

        
                public com.fin_sif.sb.types.SBResponse aMsetHDBsubscriptions
                (
                  com.fin_sif.sb.types.ADSetHDBSubscriptions aDSetHDBSubscriptions
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param onMessage
         */

        
                public void onMessage
                (
                  com.fin_sif.sb.types.OnMessage onMessage
                 )
            ;
        
         
        /**
         * Auto generated method signature
         * 
                                    * @param sBRegisterAndSubscribe
         */

        
                public com.fin_sif.sb.types.SBResponse sBregisterandsubscribe
                (
                  com.fin_sif.sb.types.SBRegisterAndSubscribe sBRegisterAndSubscribe
                 )
            ;
        
         }
    