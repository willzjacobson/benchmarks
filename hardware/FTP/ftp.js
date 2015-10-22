
'use strict';
var Promise = require('bluebird'),
    fs = require('fs'),
    config = require('./config.js'),
    levelup = Promise.promisifyAll(require('levelup')),
    db = levelup(config.dbpath),
    leveldown = require('leveldown'),
    cloudPush = require('../AWS_KINESIS/producer_app.js').cloudPush,
    rget = require('rget-jsftp'),
    path = require('path')



// converter.on("end_parsed", function(jsonArray){
//     console.log(jsonArray)

//     return jsonArray
// })


var store = function(obj){
    var timestamp = Date.now()
    obj.timestamp = timestamp
    db.put(timestamp, JSON.stringify(obj), function(err){
        if(err) throw err;
        db.get(timestamp, function(err, value){
            if(err) throw err;
        })
    })
}



 



var push = function(obj){
    obj.partitionkey =  process.env.FTPBOX || 'FTP_345PARK'
    cloudPush(obj);
}



var downloadPush = function() {
    rmDir(config.localDownloadDirectory, false)
    var rgetClient = rget.RGet(config.credentials);
    var ctx = rgetClient.generateDownloadContext('ACS', config.localDownloadDirectory);

    rgetClient.download(ctx);
    ctx.on('downloadFinished', function(file) {
        fs.readFile(path.join(config.localDownloadDirectory, ("/" + file.name)), 'utf-8', function(err, data) {
            if (err) console.log(err);
            push({data: data, filename: file.name, timezone: config.timezone})
        })
    })

    ctx.on('error', function(err){
        console.log(err)
    })
}






var dump = function() {
    db.createReadStream()
        .on('data', function(data) {
            push(data.value);
        })

    .on('close', function() {
        leveldown.destroy('/bacdata', function(err) {
            if (err) console.log(err)
        })
    })
}


var rmDir = function(dirPath, removeSelf) { //remove dir recursively (synchronous), call rmDir('path/to/dir', false) to remove all inside but not dir itself
    if (removeSelf === undefined)
        removeSelf = true;
    try {
        var files = fs.readdirSync(dirPath);
    } catch (e) {
        return;
    }
    if (files.length > 0)
        for (var i = 0; i < files.length; i++) {
            var filePath = dirPath + '/' + files[i];
            if (fs.statSync(filePath).isFile())
                fs.unlinkSync(filePath);
            else
                rmDir(filePath);
        }
    if (removeSelf)
        fs.rmdirSync(dirPath);
};




module.exports = {
    store: store,
    push: push,
    downloadPush: downloadPush,
    dump: dump
}