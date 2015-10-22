'use strict';

var Promise = require("bluebird"),
    config = require('./config.js'),
    levelup = Promise.promisifyAll(require('levelup')),
    db = levelup(config.dbpath),
    fs = Promise.promisifyAll(require('fs')),
    child_process = require('child-process-promise').spawn,
    shellCommand = child_process(config.command, config.args, {capture: ['stdout', 'stderr']}),
    cloudPush = require('../AWS_KINESIS/producer_app.js').cloudPush,
    leveldown = require('leveldown')

var count = 0;
var poll = function(){
    console.log('call count : ', count++);
     return shellCommand.then(function(result){
            return result.stdout;
        })
}


var store = function(obj){
    var timestamp = Date.now()
    obj.timestamp = timestamp
    db.put(timestamp, JSON.stringify(obj), function(err){
        if (err) throw err;
        db.get(timestamp, function(err, value){
            if (err) throw err;
            console.log('record stored in DB : ', value)
        })
    })
}


var push = function(obj){
    cloudPush(obj);
}


var dump = function() {
db.createReadStream()
    .on('data', function(data) {
        push(data.value);

    })
    .on('close', function() {
        leveldown.destroy('/moddata', function(err) {
            if (err) console.log(err);
        })
    })
}





module.exports = {
    poll: poll,
    store: store,
    push: push,
    dump: dump
}