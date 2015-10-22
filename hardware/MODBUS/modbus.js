'use strict';

var Promise = require("bluebird"),
    config = require('./config.js'),
    levelup = Promise.promisifyAll(require('levelup')),
    db = levelup(config.dbpath),
    fs = Promise.promisifyAll(require('fs')),
    child_process = require('child-process-promise').spawn,
    shellCommand = child_process('echo', ['hello'], {capture: ['stdout', 'stderr']}),
    cloudPush = require('../AWS_KINESIS/producer_app.js').cloudPush,
    leveldown = require('leveldown')



var poll = function() {
    return shellCommand
    .then(function(result) {
        return {data: result.stdout};
    })

    .fail(function(err){
        console.error(err)
    })
}


var store = function(obj) {
    var timestamp = Date.now()
    obj.timestamp = timestamp
    db.put(timestamp, JSON.stringify(obj), function(err) {
        if (err) throw err;
        db.get(timestamp, function(err, value) {
            if (err) throw err;
        })
    })

}


var push = function(obj) {
    obj.partitionkey =  process.env.MODBOX || 'MODBUS_345PARK'
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
            leveldown.destroy('/moddata', function(err) {
                if (err) console.log(err);
            })
        })
}


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
