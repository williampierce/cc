'use strict';

var path = require('path');
var _    = require('lodash');

var common = {
    server_port : 8001,
    upload_sample_path : '/upload_sample'
};

var server = {
    sample_files_dir : path.join(__dirname, '../data/wav'),
    maint_touch_file_path : path.join(__dirname, '../data/maint_requested'),
};

var device = {
    // Default setting for testing with localhost
    server_ip : '127.0.0.1',
    sample_files_dir : path.join(__dirname, '../device/tmp'),
};

exports.server_config = _.merge(server, common);
exports.device_config = _.merge(device, common);

