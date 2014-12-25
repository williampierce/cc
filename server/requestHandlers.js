// requestHandlers.js
//
// Provide a function for each type of request, as determined by the router, typically
// by examining the pathname.

var util        = require("util");
var querystring = require("querystring");
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

exports.test            = test;
exports.reportState     = reportState;
exports.getNetworkState = getNetworkState;
exports.setState        = setState;
