'use strict';

var util = require('util');
var logger = require('./logger.js');
var crypto = require('crypto');
var fs = require('fs');
var path = require('path');

function sampleProducer(kinesis, config, driverObj) {
  var log = logger().getLogger('sampleProducer');


  function _createStreamIfNotCreated(callback) {
    var params = {
      ShardCount : config.shards,
      StreamName : config.stream
    };

    kinesis.createStream(params, function(err, data) {
      if (err) {
        if (err.code !== 'ResourceInUseException') {
          callback(err);
          return;
        }
        else {
          log.info(util.format('%s stream is already created. Re-using it.', config.stream));
        }
      }
      else {
        log.info(util.format("%s stream doesn't exist. Created a new stream with that name ..", config.stream));
      }

      // Poll to make sure stream is in ACTIVE state before start pushing data.
      _waitForStreamToBecomeActive(callback);
    });
  }

  function _waitForStreamToBecomeActive(callback) {
    kinesis.describeStream({StreamName : config.stream}, function(err, data) {
      if (!err) {
        log.info(util.format('Current status of the stream is %s.', data.StreamDescription.StreamStatus));
        if (data.StreamDescription.StreamStatus === 'ACTIVE') {
          callback(null);
        }
        else {
          setTimeout(function() {
            _waitForStreamToBecomeActive(callback);
          }, 1000 * config.waitBetweenDescribeCallsInSeconds);
        }
      }
    });
  }

  function _writeToKinesis() {
    var record = driverObj;
    var cipher = crypto.createCipher('aes256', 'letmein345');
    record = cipher.update(JSON.stringify(record), 'utf8', 'base64');
    record += cipher.final('base64');
    var key = fs.readFileSync(path.join(__dirname + '/key.pem'));
    var sign = crypto.createSign('RSA-SHA256');
    var signed = sign.update(record);
    signed = sign.sign(key, 'base64');
    var kinesisObj = JSON.stringify({record: record, signature: signed})
    var recordParams = {
      Data : kinesisObj,
      PartitionKey : driverObj.partitionkey,
      StreamName : config.stream
    };

    kinesis.putRecord(recordParams, function(err, data) {
      if (err) {
        log.error(err);
        throw (err);
      }
      else {
        log.info('Successfully sent data to Kinesis.');
      }
    });
  }

  return {
    run: function() {
      _createStreamIfNotCreated(function(err) {
        if (err) {
          log.error(util.format('Error creating stream: %s', err));
          console.log(err)
          return;
        }


          _writeToKinesis();

        
      });
    }
  };
}

module.exports = sampleProducer;