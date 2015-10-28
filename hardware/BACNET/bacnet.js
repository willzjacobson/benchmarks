'use strict';

var Promise = require("bluebird"),
    config = require('./config.js'),
    levelup = Promise.promisifyAll(require('levelup')),
    db = levelup(config.dbpath),
    fs = Promise.promisifyAll(require('fs')),
    child_process = require('child-process-promise').spawn,
    shellCommand = child_process(config.command, config.args, {capture: ['stdout', 'stderr']}),
    cloudPush = require('../AWS_KINESIS/producer_app.js').cloudPush,
    leveldown = require('leveldown'),
    path = require('path'),
    excel = require('excel');



var poll = function(deviceID){
     return child_process(config.command, [config.args[0], deviceID], {capture: ['stdout', 'stderr']})
     .then(function(result){
            fs.appendFile(process.env.bacnetoutpath, result.stdout, function(err){console.log(err)});
        console.log(result.stdout)
        return {data: result.stdout};
        })
     .fail(function(err){
        console.error(err)
     })
}


var store = function(obj){
    var timestamp = Date.now()
    obj.timestamp = timestamp
    db.put(timestamp, JSON.stringify(obj), function(err){
        if (err) throw err;
    })
}


var push = function(obj){
    obj.partitionkey = process.env.BACNETBOX || 'BACNET_345PARK'
    cloudPush(obj);
}


var devpush = function(obj){
    console.log(obj)
}

var dump = function() {
    db.createReadStream()
        .on('data', function(data) {
            devpush(data.value);
        })
        .on('close', function() {
            leveldown.destroy('/bacdata', function(err) {
                if (err) console.log(err)
            })
        })
}

/* root@192.168.98.145 "../data/protocol_drivers/bacnet-stack-0.8.2/demo/epics/bacepics -v */
//2933673

// poll()
// var rmDir = function(dirPath, removeSelf) { //remove dir recursively (synchronous), call rmDir('path/to/dir', false) to remove all inside but not dir itself
//     if (removeSelf === undefined)
//         removeSelf = true;
//     try {
//         var files = fs.readdirSync(dirPath);
//     } catch (e) {
//         return;
//     }
//     if (files.length > 0)
//         for (var i = 0; i < files.length; i++) {
//             var filePath = dirPath + '/' + files[i];
//             if (fs.statSync(filePath).isFile())
//                 fs.unlinkSync(filePath);
//             else
//                 rmDir(filePath);
//         }
//     if (removeSelf)
//         fs.rmdirSync(dirPath);
// };  





module.exports = {
    poll: poll,
    store: store,
    push: push,
    dump: dump
}

