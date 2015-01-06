var request = require('superagent');
var mraa = require('mraa');
var config = require('../common/config').device_config;

// Config
var blinkPin = 13;       // On the Edison Arduino breakout, this flashes an onboard LED
var blinkTimeout = 1000; // 2 second period

// State
var blinkEnabled = false;
var blinkState = false;

// Initialization
var blinkLed = new mraa.Gpio(blinkPin);
blinkLed.dir(mraa.DIR_OUT);

function blinkLoop()
{
    blinkLed.write((blinkEnabled && blinkState) ? 1 : 0);
    blinkState = !blinkState;
    setTimeout(blinkLoop, blinkTimeout);
}

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
                var state = res.body;
                //console.log('Received: ' + JSON.stringify(state));

                if('maintRequested' in state) {
                    if(blinkEnabled != state.maintRequested) {
                        console.log('Setting blinkEnabled to ' + state.maintRequested);
                        blinkEnabled = state.maintRequested;
                    }
                }
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

blinkLoop();
mainLoop();

