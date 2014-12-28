'use strict';

var path = require('path');
var _    = require('lodash');

var common = {
    server_port : 8001,
    upload_sample_path : '/upload_sample'
};

var server = {
    sample_files_dir : path.join(__dirname, '../tmp'),
};

var device = {
    server_ip : '192.168.1.100',
    sample_files_dir : path.join(__dirname, '../tmp'),
};

exports.server_config = _.merge(common, server);
exports.device_config = _.merge(common, device);

