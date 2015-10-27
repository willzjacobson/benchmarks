'use strict';

var AWS = require('aws-sdk');
var config = require('./config');
var producer = require('./sample_producer');





var kinesis = new AWS.Kinesis({region : config.kinesis.region});
var cloudPush = function(driverObj){
	producer(kinesis, config.sampleProducer, driverObj).run();
}


module.exports = {
	cloudPush: cloudPush
}


