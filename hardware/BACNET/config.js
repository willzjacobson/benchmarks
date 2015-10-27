'use strict';
var path = require('path')
var config = module.exports = {
  command: process.env.bacnetCMD || 'echo',
  args: [process.env.bacnetARG1, process.env.bacnetARG2] || ['This is bacnet data'],
  dbpath: process.env.BACSTORAGEPATH || path.join(__dirname, "/bacdata"),
  controllerList: ['3689119',
  '4098468',
  '4098467',
  '1',
  '3',
  '4',
  '2',
  '5',
  '3990548',
  '4110103',
  '3990608',
  '4138819',
  '457039',
  '457040',
  '475041',
  '457042',
  '4032264',
  '3807119',
  '4010043',
  '3975916',
  '4009787',
  '4030322',
  '4009416',
  '4007559',
  '3979700',
  '4009413',
  '4007179',
  '4009408',
  '4042872',
  '4042869',
  '4042733',
  '3976013',
  '4042732',
  '4042339',
  '4043082',
  '4042338',
  '3990656',
  '4043079',
  '3976014',
  '4032547',
  '4042399',
  '3452002',
  '4010071',
  '4042326',
  '4009806',
  '4040665',
  '4009803',
  '3992910',
  '4009491',
  '3992701',
  '4009488']
};







/*
  3689119 C0:A8:02:CF:BA:C0    0     00                   1476                                                                               
  4098468 C0:A8:02:C8:BA:C0    0     00                   1476                                                                               
  4098467 C0:A8:02:D0:BA:C0    0     00                   1476                                                                               
  1       A9:FE:01:02:BA:C0    0     00                   1350                                                                               
  3       C0:A8:02:C9:BA:C0    0     00                   1350                                                                               
  4       C0:A8:02:CA:BA:C0    0     00                   1350                                                                               
  2       C0:A8:02:C6:BA:C0    0     00                   1350                                                                               
  5       C0:A8:02:CB:BA:C0    0     00                   1350                                                                               
  3990548 C0:A8:02:C5:BA:C0    0     00                   1476                                                                               
  4110103 C0:A8:02:CE:BA:C0    0     00                   1476                                                                               
  3990608 C0:A8:02:CD:BA:C0    0     00                   1476                                                                               
  4138819 C0:A8:02:D1:BA:C0    0     00                   1476                                                                               
  457039  C0:A8:02:C8:BA:C0    2768  27                   480                                                                                
  457040  C0:A8:02:C8:BA:C0    2768  28                   480                                                                                
  475041  C0:A8:02:C8:BA:C0    2768  29                   480                                                                                
  457042  C0:A8:02:C8:BA:C0    2768  2A                   480                                                                                
  4032264 C0:A8:02:CD:BA:C0    2766  02                   478                                                                                
  3807119 C0:A8:02:C5:BA:C0    2765  23                   478                                                                                
  4010043 C0:A8:02:CD:BA:C0    2766  03                   478                                                                                
  3975916 C0:A8:02:C5:BA:C0    2765  24                   478                                                                                
  4009787 C0:A8:02:CD:BA:C0    2766  04                   478                                                                                
  4030322 C0:A8:02:C5:BA:C0    2765  25                   478                                                                                
  4009416 C0:A8:02:CE:BA:C0    2767  1C                   478                                                                                
  4007559 C0:A8:02:CD:BA:C0    2766  05                   478                                                                                
  3979700 C0:A8:02:C5:BA:C0    2765  26                   478                                                                                
  4009413 C0:A8:02:CE:BA:C0    2767  1D                   478                                                                                
  4007179 C0:A8:02:CD:BA:C0    2766  06                   478                                                                                
  4009408 C0:A8:02:CE:BA:C0    2767  1E                   478  
  4042872 C0:A8:02:C5:BA:C0    2765  01                   478                                                                                
  4042869 C0:A8:02:C5:BA:C0    2765  02                   478  
  4042733 C0:A8:02:C5:BA:C0    2765  03                   478                                                                                
  3976013 C0:A8:02:CD:BA:C0    2766  09                   478                                                                                
  4042732 C0:A8:02:C5:BA:C0    2765  04                   478                                                                                
  4042339 C0:A8:02:C5:BA:C0    2765  05                   478                                                                                
  4043082 C0:A8:02:CD:BA:C0    2766  0B                   478                                                                                
  4042338 C0:A8:02:C5:BA:C0    2765  06                   478                                                                                
  3990656 C0:A8:02:CE:BA:C0    2767  23                   478                                                                                
  4043079 C0:A8:02:CD:BA:C0    2766  0C                   478                                                                                
  3976014 C0:A8:02:CE:BA:C0    2767  24                   478                                                                                
  4032547 C0:A8:02:C5:BA:C0    2765  07                   478                                                                                
  4042399 C0:A8:02:CD:BA:C0    2766  0D                   478                                                                                
  3452002 C0:A8:02:CE:BA:C0    2767  25                   478                                                                                
  4010071 C0:A8:02:C5:BA:C0    2765  08                   478                                                                                
  4042326 C0:A8:02:CD:BA:C0    2766  0E                   478                                                                                
  4009806 C0:A8:02:C5:BA:C0    2765  09                   478                                                                                
  4040665 C0:A8:02:CD:BA:C0    2766  0F                   478                                                                                
  4009803 C0:A8:02:C5:BA:C0    2765  0A                   478                                                                                
  3992910 C0:A8:02:CE:BA:C0    2767  26                   478                                                                                
  4009491 C0:A8:02:C5:BA:C0    2765  0B                   478                                                                                
  3992701 C0:A8:02:CE:BA:C0    2767  27                   478                                                                                
  4009488 C0:A8:02:C5:BA:C0    2765  0C                   478                                                                                 

/*


    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7403)
    object-name: "PumpFail.13"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7404)
    object-name: "PumpFail.19"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7405)
    object-name: "PumpFail.20"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7406)
    object-name: "PumpFail.23"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7407)
    object-name: "PumpFail.24"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7408)
    object-name: "PumpFail.25"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7409)
    object-name: "PumpFail.26"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7410)
    object-name: "PumpFail.CHWP"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7411)
    object-name: "PumpFail.CWP"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7412)
    object-name: "PumpFail.P1"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7413)
    object-name: "PumpFail.P10"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7414)
    object-name: "PumpFail.P11"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7415)
    object-name: "PumpFail.P16"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7416)
    object-name: "PumpFail.P17"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7417)
    object-name: "PumpFail.P18"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7418)
    object-name: "PumpFail.P2"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7419)
    object-name: "PumpFail.P3"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7420)
    object-name: "PumpFail.P33"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7421)
    object-name: "PumpFail.P34"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7422)
    object-name: "PumpFail.P35"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7423)
    object-name: "PumpFail.P36"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7424)
    object-name: "PumpFail.P37"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7425)
    object-name: "PumpFail.P38"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7426)
    object-name: "PumpFail.P39"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7427)
    object-name: "PumpFail.P4"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7428)
    object-name: "PumpFail.P40"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7429)
    object-name: "PumpFail.P5"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7430)
    object-name: "PumpFail.P6"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7431)
    object-name: "PumpFail.P7"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7432)
    object-name: "PumpFail.P8"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7433)
    object-name: "PumpFail.P9"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7434)
    object-name: "RHCStptEast.S7"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7435)
    object-name: "RHCStptEast.S1"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7436)
    object-name: "RHCStptNorth.S2"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7437)
    object-name: "RHCStptNorth.S8"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7438)
    object-name: "RHCStptSouth.S7"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7439)
    object-name: "RHCStptSouth.S1"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7440)
    object-name: "RHCStptWest.S2"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7441)
    object-name: "RHCStptWest.S8"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 45.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,45.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7442)
    object-name: "S10_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7443)
    object-name: "S11_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7444)
    object-name: "S12_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7445)
    object-name: "S13_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7446)
    object-name: "S14_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7447)
    object-name: "S15_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7448)
    object-name: "S16_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 55.400002
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,55.400002,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7449)
    object-name: "S17_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7450)
    object-name: "S18_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7451)
    object-name: "S19_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 57.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,57.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7452)
    object-name: "S1_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 47.500000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,47.500000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7453)
    object-name: "S20_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7454)
    object-name: "S22_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 54.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,54.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7455)
    object-name: "S2_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 51.099998
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,51.099998,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7456)
    object-name: "S3_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7457)
    object-name: "S4_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7458)
    object-name: "S5_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7459)
    object-name: "S6_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7460)
    object-name: "S7_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 50.099998
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,50.099998,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7461)
    object-name: "S8_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7462)
    object-name: "S9_FanFdbck"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 60.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,60.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7463)
    object-name: "SESupStptCalc34"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 56.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,56.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7464)
    object-name: "SESupStptCalc9"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 56.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,56.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7465)
    object-name: "Steam.Momentary"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 55.200001
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,55.200001,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7466)
    object-name: "SteamTempHiBoth"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7467)
    object-name: "StmHi.Momentary"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7468)
    object-name: "StmLow.Momentary"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 20.400000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,20.400000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7469)
    object-name: "StmMed.Momentary"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 34.799999
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,34.799999,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7470)
    object-name: "TCT1.HighTemp"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7471)
    object-name: "TCT2.HighTemp"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 0.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,0.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7472)
    object-name: "Total.Demand"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 6356.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,6356.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7473)
    object-name: "Water.TodayCF"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 12762.000000
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,12762.000000,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    COV-increment: 0.000000
    description: ""
    event-state: normal
    object-identifier: (Analog Value, 7474)
    object-name: "Water.TodayG"
    object-type: Analog Value
    out-of-service: FALSE
    present-value: 43902.898438
    priority-array: { Null,Null,Null,Null,Null,Null,Null,Null,Null,43902.898438,Null,Null,Null,Null,Null,Null }
    relinquish-default: 0.000000
    status-flags: {false,false,false,false}
    units: no-units
  },
  {
    archive: FALSE Writable
    file-access-method: 1
    file-size: 0
    file-type: "Configuration"
    modification-date: { (7-Feb-2106, 7),06:28:15.00 }
    object-identifier: (File, 1)
    object-name: "ACCConfiguration"
    object-type: File
    read-only: TRUE
  },
  {
    description: ""
    object-identifier: (Program, 7003)
    object-name: "Randomize"
    object-type: Program
    out-of-service: FALSE
    program-change: 0 Writable
    program-state: 2
    status-flags: {false,false,false,false}
  }
}
End of BACnet Protocol Implementation Conformance Statement

*/