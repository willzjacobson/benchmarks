'use strict';

var express = require('express'),
    app = express(),
    http = require('http'),
    server = http.createServer(app),
    xmlparser = require('express-xml-bodyparser'),
    morgan = require('morgan'),
    fs = require('fs'),
    config = require('./config.js'),
    leveldown = require('leveldown'),
    levelup = require('levelup'),
    db = levelup(config.dbpath),
    crypto = require('crypto'),
    Promise = require('bluebird'),
    cloudPush = require('../AWS_KINESIS/producer_app.js').cloudPush,
    o2x = require('object-to-xml'),
    AWS = require('aws-sdk')

AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
})
// app.use(express.json());
// app.use(express.urlencoded());
app.set('port', process.env.PORT || 8080);
app.use(xmlparser());
var accessLogStream = fs.createWriteStream(__dirname + '/access.log', {
    flags: 'a'
})
app.use(morgan('combined', {
    stream: accessLogStream
}))



app.post('/211/', function(req, res, next) {

    var obj = {
        '?xml version=\"1.0\"?': null,
        DAS: {
            result: 'SUCCESS'
        }
    }

    var record = {data: req.body}
    record.partitionkey = process.env.XMLBOX || 'XML_345PARK'
    cloudPush(record)

    res.set('Content-Type', 'text/xml');
    res.send(o2x(obj));
});


app.use(function(err, req, res, next) {
    console.error(err.stack);
    res.status(500).send('Error');
});



var startServer = function() {
    server.listen(app.get('port'), function() {
        console.log("SERVER IS ALIVE!!!")
    });
}



module.exports = {startServer: startServer}

//66.17.177.245
