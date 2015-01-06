var fs = require('fs');
var path = require('path');
var url = require('url');
var request = require('superagent');
var config = require('../common/config').device_config;

function checkMaintRequested()
{
    request
        .post(config.server_ip + ':' + config.server_port + '/exchange_device_state')
        .set('Content-Type', 'application/json')
        .set('Accept', 'application/json')
        .send({})
        .end(function(err, res) {
            if(err) {
                console.log('Error: ' + err.message);
            }
            else if(res.ok) {
                console.log('Received: ' + JSON.stringify(res.body));
            }
            else {
                console.log('Error: ' + res.text);
            }
        });
}

function mainLoop()
{
    checkMaintRequested();

    setTimeout(mainLoop, 5000);
}

mainLoop();

