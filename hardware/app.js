'use strict';

global.connectionState = true; //GLOBAL CONNECTIVITY STATE VARIABLE
var Promise = require('bluebird'),
    bacnet = Promise.promisifyAll(require('./BACNET/bacnet.js')),
    modbus = Promise.promisifyAll(require('./MODBUS/modbus.js')),
    opc = Promise.promisifyAll(require('./OPC/opc.js')),
    ftp = require('./FTP/ftp.js'),
    xmlserver = require('./XML/xml.js').startServer,
    config = require('./config.js'),
    CronJob = require('cron').CronJob,
    dns = Promise.promisifyAll(require('dns'))

xmlserver()

var callCount = 0;
var testConnection = function() {
    dns.resolveAsync('www.google.com')
        .then(function() {
            if (global.connectionState === false) {
                console.log('connection was reconnected')
                bacnet.dump();
                modbus.dump();
                opc.dump();
                global.connectionState = true; //on reconnect set connection state to true
            }

            console.log('connection is active. call count : ', callCount++)

            bacnet.poll().then(function(data) { //push directly if connection is fine
                bacnet.push(data);
            });

            //hello

            // modbus.poll().then(function(data) {
            //     console.log(data)
            //     modbus.push(data);
            // });

            // opc.poll().then(function(data) {
            //     opc.push(data)
            // });

            ftp.downloadPush()
        })

    .error(function() {
        global.connectionState = false; //storing logic on connection failure
        console.log('not connected')

        bacnet.poll().then(function(data) {
            bacnet.store(data);
        });

        // modbus.poll().then(function(data) {
        //     modbus.store(data);
        // });

        // opc.poll().then(function(data) {
        //     opc.store(data);
        // });

        ftp.downloadAsync().then(function(data) {
            ftp.store(data)
        })

    })
}




new CronJob('*/5 * * * *', function() {

    testConnection();

}, null, true, 'America/New_York');
