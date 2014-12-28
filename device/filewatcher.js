var fs = require('fs');
var http = require('http');
var path = require('path');
var config = require('../common/config').device_config;

function uploadFile(sample_file)
{
    var options = {
        host: config.server_ip,
        port: config.server_port,
        path: config.upload_sample_path + "?filename=" + path.basename(sample_file),
        method: 'POST'
    };

    var req = http.request(options, function(res) {
        console.log('STATUS: ' + res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('BODY: ' + chunk);
        });
    });

    req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
    });

    var input = fs.createReadStream(sample_file);

    input.on('data', function (chunk) {
       req.write(chunk, 'binary');
    });

    input.on('end', function() {
        req.end();
    });

    input.on('error', function(err) {
        console.log('Error: ' + err);
        req.end(err);
    });
}

function uploadSamples()
{
    // Upload, then delete, any .wav files to the server
    
    // Quick test
    var sample_file = path.join(config.sample_files_dir, "test.wav");
    uploadFile(sample_file);
}

console.log('sample_files_dir: ' + config.sample_files_dir);

// Any time there is an fs event for the samples directory, call uploadSamples() to
// check for new additions.
fs.watch(config.sample_files_dir, function (event, filename) {
    console.log('fs.watch file: ' + filename + ', event: ' + event);
    uploadSamples();
});
