// deviceControl.js
//     Provides functions for sending http requests to control devices

var http = require('http');


// Send request to update device state
//     Uses agent id to determine URL; sends device state as JSON
//     state:
//         agentId: <agent id string>
//         face:    1..6
function setState(state)
{
    var jsonState = JSON.stringify(state);

    var headers = {
        'Content-Type': 'application/json',
        'Content-Length': jsonState.length
    };

    var options = {
        host: 'agent.electricimp.com',
        port: 80,
        // Example path: '/ck2d15weoILd/setState',
        path: '/' + state.agentId + '/setState',
        method: 'POST',
        headers: headers
    };

    console.log("Sending setState request...");
    console.log("    Options: " + JSON.stringify(options));
    console.log("    State:   " + JSON.stringify(state));

    var request = http.request(options, function(res) {
            console.log("Response from setState request:");
            console.log('    STATUS: ' + res.statusCode);
            console.log('    HEADERS: ' + JSON.stringify(res.headers));
            res.setEncoding('utf8');
            res.on('data', function (chunk) {
                console.log('    BODY: ' + chunk);
                });
            });

    request.on('error', function(e) {
            console.log('Error for setState request: ' + e);
            });

    request.write(jsonState);
    request.end();
}

exports.setState = setState;
