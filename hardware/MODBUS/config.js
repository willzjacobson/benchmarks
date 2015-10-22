'use strict';
var path = require('path')
var config = module.exports = {
    command: 'python',
    args: ['/data/protocol_drivers/pymodbus/pymodbus/ModbusClient.py'],
    dbpath: process.env.MODSTORAGEPATH || path.join(__dirname, '/moddata')
};
