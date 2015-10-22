'use strict';
var path = require('path');
var config = module.exports = {
    credentials: {
        host: 'ftp.di-boss.com',
        port: 21,
        username: 'integra',
        password: 'int!egra1'
    },

    ftpOptions: {
        logging: 'basic',
        overwrite: 'none'
    },

    dbpath: process.env.FTPSTORAGEPATH || path.join(__dirname, '/ftpdata'),

    directory: 'ACS',

    localDownloadDirectory: path.join(__dirname , '/downloads'),

    timezone: "America/New_York"
}

