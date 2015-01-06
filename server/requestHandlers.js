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


// *** Device to Server ***

function exchangeDeviceState(request, query, data, response)
{
    if(!data) {
        console.log('Empty data');
        var headers = {
            'Content-Type': 'text/plain'
        };
        response.writeHead(400, headers);
        response.end('400 Bad request');
        return;
    }
    var uploadState = JSON.parse(data); 
    var downloadState = logic.exchangeDeviceState(uploadState);

    var jsonData = JSON.stringify(downloadState);

    var headers = {
        'Content-Type': 'application/json',
        'Content-Length': jsonData.length
    };

    response.writeHead(200, headers);
    response.end(jsonData);
}


// *** Operator to Server ***

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
        logic.setMaintRequested(true);
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
        logic.setMaintRequested(false);
        fs.unlink(config.maint_touch_file_path, function (err) { /* ignore err for missing file */ });
        console.log('Maintenance light turned off');
        response.write('Maintenance light turned off');
    }

    response.end();
}

exports.test                = test;
exports.sampleList          = sampleList;
exports.setMaintenanceLight = setMaintenanceLight;
exports.exchangeDeviceState = exchangeDeviceState;
