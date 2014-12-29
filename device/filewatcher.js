var fs = require('fs');
var path = require('path');
var http = require('http');
var config = require('../common/config').device_config;

function uploadAndDeleteFile(file_path)
{
    var options = {
        host: config.server_ip,
        port: config.server_port,
        path: config.upload_sample_path + "?filename=" + path.basename(file_path),
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

    var input = fs.createReadStream(file_path);

    input.on('data', function (chunk) {
       req.write(chunk, 'binary');
    });

    input.on('end', function() {
        fs.unlink(file_path);
        req.end();
    });

    input.on('error', function(err) {
        console.log('Error: ' + err.message);
        req.end(err.message);
    });
}

function uploadAndDeleteFiles(dir_path)
{
    // Upload, then delete, any .wav files to the server
    fs.readdir(dir_path, function(err, files) {
        if(err) {
            console.log('readdir failed: ' + err);
            return;
        }
        for(var i = 0; i < files.length; i++) {
            console.log('Found sample: ' + files[i]);
            uploadAndDeleteFile(path.join(dir_path, files[i]));
        }
    });
}

console.log('sample_files_dir: ' + config.sample_files_dir);

// Any time there is an fs event for the samples directory, call uploadSamples() to
// check for new additions.
fs.watch(config.sample_files_dir, function (event, filename) {
    console.log('fs.watch file: ' + filename + ', event: ' + event);
    uploadAndDeleteFiles(config.sample_files_dir);
});
