var fs     = require("fs");
var config = require("../common/config").server_config;
var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}

// Make sure binary files directory exists before proceeding.
if(!fs.exists(config.sample_files_dir))
{
    console.log("Creating sample files directory: " + config.sample_files_dir);
    fs.mkdirSync(config.sample_files_dir);
}

// Test/debug
handle["/test"]            = requestHandlers.test;

// Agent requests
handle[config.upload_sample_path] = requestHandlers.uploadSample;
handle["/reportState"]            = requestHandlers.reportState;

// User requests
handle["/getNetworkState"] = requestHandlers.getNetworkState;
handle["/setState"]        = requestHandlers.setState;

server.start(router.route, handle);
