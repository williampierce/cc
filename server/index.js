var fs     = require("fs");
var config = require("../common/config").server_config;
var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}

// Make sure binary files directory exists before proceeding.
try
{
    console.log("Creating sample files directory (if necessary): " + config.sample_files_dir);
    fs.mkdirSync(config.sample_files_dir);
}
catch(error)
{
    //console.log(error.message);
}

// Test/debug
handle["/test"] = requestHandlers.test;

// Device requests
handle["/exchange_device_state"] = requestHandlers.exchangeDeviceState;

// User requests
handle["/sample_list"]           = requestHandlers.sampleList;
handle["/set_maintenance_light"] = requestHandlers.setMaintenanceLight;  

server.start(router.route, handle);
