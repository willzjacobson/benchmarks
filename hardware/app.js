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
var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/debug.log', {flags : 'w'});
var log_stdout = process.stdout;

console.log = function(d) { //
  log_file.write(util.format(d) + '\n');
  log_stdout.write(util.format(d) + '\n');
};
  var controllerList = ['3689119',
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
// xmlserver()

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


            var i = controllerList.length - 1
            function timeout() {
                setTimeout(function() {
                    bacnet.poll(controllerList[i]).then(function(data) {
                         //push directly if connection is fine
                        bacnet.push(data);
                        i--
                    }); //  your code here
                    if(i >= 0 ){
                     timeout(); 
                 } else {
                    return;
                 }
                }, 180000);
            }

            
            timeout();
            //hello

            // modbus.poll().then(function(data) {
            //     console.log(data)
            //     modbus.push(data);
            // });

            // opc.poll().then(function(data) {
            //     opc.push(data)
            // });

            // ftp.downloadPush()
        })

    .error(function() {
        global.connectionState = false; //storing logic on connection failure
        console.log('not connected')

        bacnet.poll()
        .then(function(data) {
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




// new CronJob('*/5 * * * *', function() {

    testConnection();

// }, null, true, 'America/New_York');
