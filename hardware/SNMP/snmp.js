'use strict';

// var snmp = require('net-snmp');
// var session = new snmp.Session({ host: 'localhost', port: 161, community: 'public' });

/*


-- $Id: obvius-mib.txt,v 1.2 2004/10/18 17:06:07 herzogs Exp $ --
OBVIUSTRAP     DEFINITIONS ::=  BEGIN
IMPORTS
    enterprises
        FROM RFC1155-SMI
    DisplayString
        FROM RFC1213-MIB
    OBJECT-TYPE
        FROM RFC-1212
    TRAP-TYPE
        FROM RFC-1215;
-- The following object tree is for the Obvius Trap objects. --
    obvius            OBJECT IDENTIFIER ::=  {enterprises 15115 } 
    acquisuite        OBJECT IDENTIFIER ::=  {obvius 1 }
    acquilite         OBJECT IDENTIFIER ::=  {obvius 2 }
serialnumber  OBJECT-TYPE
    SYNTAX      DisplayString
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The serial number of the AcquiSuite reporting an alarm. This is also the MAC address."
    ::= { acquisuite 1 }
modbusaddress  OBJECT-TYPE
    SYNTAX      INTEGER
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The modbus address of the device reported."
    ::= { acquisuite 2 }
devicename  OBJECT-TYPE
    SYNTAX      DisplayString
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The name of the device reported."
    ::= { acquisuite 3 }
    
pointnumber  OBJECT-TYPE
    SYNTAX      INTEGER
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The number of the point reported. zero based."
    ::= { acquisuite 4 }
pointname  OBJECT-TYPE
    SYNTAX      DisplayString
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The name of the point reported."
    ::= { acquisuite 5 }
pointvalue  OBJECT-TYPE
    SYNTAX      DisplayString
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The value of the point reported."
    ::= { acquisuite 6 }
pointunits  OBJECT-TYPE
    SYNTAX      DisplayString
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "The engineering units for the value reported."
    ::= { acquisuite 7 }
alarmtype  OBJECT-TYPE
    SYNTAX      INTEGER { 
                          noError(0),
                          deviceError(1),
                          lowAlarm(2),
                          highWarn(3),
                          highAlarm(4) }
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Reasons for the alarm."
    ::= { acquisuite 8 }
END

*/