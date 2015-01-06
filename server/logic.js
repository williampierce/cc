var fs     = require('fs');
var config = require('../common/config').server_config;

// Contains the business logic. Maintains state based on inputs; updates device state.

// Just one bike for now. Set this according to the touch file on startup. Then update with
// server requests.
var g_maintRequested = false;

// Use synchronous calls on startup
function initSync()
{
    if(fs.existsSync(config.maint_touch_file_path))
        g_maintRequested = true;
    else
        g_maintRequested = false;
}

function setMaintRequested(value)
{
    g_maintRequested = value;
}

function exchangeDeviceState(uploadState)
{
    // Eventually, the upload state will contain at least a device id; we ignore it for now.
    var downloadState = {};

    downloadState.maintRequested = g_maintRequested;
    return downloadState;
}

exports.initSync            = initSync;
exports.setMaintRequested   = setMaintRequested;
exports.exchangeDeviceState = exchangeDeviceState;
