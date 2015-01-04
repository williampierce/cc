// requestHandlers.js
//
// Provide a function for each type of request, as determined by the router, typically
// by examining the pathname.

var fs          = require("fs");
var path        = require("path");
var util        = require("util");
var querystring = require("querystring");
var config      = require("../common/config").server_config;
var logic       = require("./logic");     // business logic


// *** Test/Debug ***
function test(request, query, data, response) 
{
    console.log("Test request...");
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write(util.inspect(request.headers));
    response.end("\r\nOK (test)");
}


// *** Device/Agent to Server ***

// not used...
// Device uploads sample file
function uploadSample(request, query, data, response)
{
    // Expects query: "filename=<filename>"
    var filename  = query['filename'];
    
    if(filename)
    {
        var file_path = path.join(config.sample_files_dir, filename);
        console.log("uploadSample, file_path: " + file_path);
    }
    else
        console.log("uploadSample, missing 'filename' field");
}

// not used...
// Agent reports device state using JSON
//     agent_id: <string>
//     face:     1..6
function reportState(request, query, data, response) 
{
    // console.log("Function reportState called, updating state...");

    var state = JSON.parse(data);
    // console.log("  state: " + state);

    logic.updateState(state);

    response.writeHead(200, {"Content-Type": "text/plain"});
    response.end("OK (reportState)");
}


// *** Operator to Server ***

// /sample_list
function sampleList(request, query, data, response)
{
    console.log("Function getSampleList called...");
    
    // Provide the client with the list of samples in the samples directory.
    fs.readdir(config.sample_files_dir, function(err, files) {
        if(err) {
            console.log('sampleList, readdir failed: ' + err);
            response.writeHead(505, {"Content-Type": "text/plain"});
            response.end("Internal server error (sampleList)");
            return;
        }
        var jsonData = JSON.stringify(files);

        var headers = {
            'Content-Type': 'application/json',
            'Content-Length': jsonData.length
        };

        response.writeHead(200, headers);
        response.end(jsonData);
    });
}

function setMaintenanceLight(request, query, data, response)
{
    console.log('setMaintenanceLight called...');

    // Expects query: "value=on|off"
    var value = query['value'].toLowerCase();

    response.writeHead(200, { 'Content-Type': 'text/plain', });

    if(value == 'on') {
        fs.open(config.maint_touch_file_path, "wx", function (err, fd) {
            if(!err) {
                fs.close(fd, function (err) {
                    if(err) {
                        console.log('Error closing file ' + config.maint_touch_file_path + ', ' + err.message);
                    }
                });
            }
        });
                         
        console.log('Maintenance light turned on');
        response.write('Maintenance light turned on');
    }
    else {
        fs.unlink(config.maint_touch_file_path, function (err) { /* ignore err for missing file */ });
        console.log('Maintenance light turned off');
        response.write('Maintenance light turned off');
    }

    response.end();
}

// not used...
// Operator requests network state
//     <server>/getNetworkState
//
// Returns JSON object. See logic.js  for details.
function getNetworkState(request, query, data, response)
{
    console.log("Function getNetworkState called...");

    var networkState = logic.getNetworkState();

    var jsonData = JSON.stringify(networkState);

    var headers = {
        'Content-Type': 'application/json',
        'Content-Length': jsonData.length
    };

    response.writeHead(200, headers);
    response.end(jsonData);
}

// not used...
// Operator sets device state using a query string
//     <server>/setState?agent_id=<string>&face=<1..6>
//
// For test, probably not needed longterm.
function setState(request, query, data, response) 
{
    console.log("Function setState called...");

    var state = querystring.parse(query);
    console.log("    query: " + query);
    if(data)
        console.log("    data:  " + data);

    logic.updateState(state);

    response.writeHead(200, {"Content-Type": "text/plain"});
    response.end("OK (setState)");
}

exports.test                = test;
exports.sampleList          = sampleList;
exports.setMaintenanceLight = setMaintenanceLight;

//exports.uploadSample    = uploadSample;
//exports.reportState     = reportState;
//exports.getNetworkState = getNetworkState;
//exports.setState        = setState;

