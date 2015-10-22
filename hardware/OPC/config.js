'use strict';
var path = require('path');
var config = module.exports = {
  command: 'echo',
  args: ['This is OPC data!'],
  dbpath: process.env.OPCSTORAGEPATH || path.join(__dirname, '/opcdata')
};