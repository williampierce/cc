var server = require("./server");
var router = require("./router");
var config = require("../common/config").server_config;
var requestHandlers = require("./requestHandlers");

var handle = {}

// Test/debug
handle["/test"]            = requestHandlers.test;

// Agent requests
handle[config.upload_sample_path] = requestHandlers.uploadSample;
handle["/reportState"]            = requestHandlers.reportState;

// User requests
handle["/getNetworkState"] = requestHandlers.getNetworkState;
handle["/setState"]        = requestHandlers.setState;

server.start(router.route, handle);
