var http      = require('http');
var url       = require('url');
var fs        = require('fs');
var path      = require('path');
var config    = require('../common/config').server_config;
var clientMgr = require('./clientMgr');

// Given a routing function and a mapping from pathnames to request handlers, this
// function will create a server to handle http requests on port config.server_port.
// If a pathname has the form "/static/<page>", then the specified page will be
// delivered and no handler will be called.
function start(route, handle)
{
    function onRequest(request, response)
    {
        var request_parse = url.parse(request.url, true);
        var pathname      = request_parse.pathname;
        var query         = request_parse.query;

        console.log("HTTP " + request.method + " request for " + pathname + " received");
        if(query)
            console.log("  Query: " + JSON.stringify(query));

        // If the request is for a static file, return it
        if(serveStaticFile(request, pathname, response))
            return;

        if(uploadBinaryFile(request, pathname, query, response))
            return;

        serveJsonRequest(route, handle, request, response);
    }

    var server = http.createServer(onRequest);
    server.listen(config.server_port); 
    console.log('Server running on port ' + config.server_port);
}

function uploadBinaryFile(request, pathname, query, response)
{
    // Handle "/upload_sample?filename=<filename>"
    if(pathname != config.upload_sample_path)
        return false;

    console.log("Uploading binary file...");

    // Expects query: "filename=<filename>"
    var filename  = query['filename'];
    
    if(!filename)
    {
        console.log("uploadBinaryFile, missing 'filename' field");
        response.writeHead(400, {"Content-Type": "text/plain"});
        response.end("Bad request"); 
        return true; // request complete
    }

    var file_path = path.join(config.sample_files_dir, filename);
    console.log("uploadBinaryFile, file_path: " + file_path);
    var output = fs.createWriteStream(file_path);

    output.on("error", function(error) { 
        console.log("Write stream error: " + error);
        response.writeHead(500, {"Content-Type": "text/plain"});
        response.end("Internal server error"); 
    });

    output.on("open", function() {
        console.log("Write stream open");

        function postData(chunk)
        {
            output.write(chunk, 'binary');
        }

        function postEnd()
        {
            output.end();
            console.log("uploadBinaryFile, upload complete");
            response.writeHead(200, {"Content-Type": "text/plain"});
            response.end("Upload successful"); 
        }

        request.setEncoding("binary");
        request.addListener("data", postData);
        request.addListener("end",  postEnd);
    });

    return true;
}

function serveJsonRequest(route, handle, request, response)
{
    var request_parse = url.parse(request.url, true);
    var pathname      = request_parse.pathname;
    var query         = request_parse.query;
    var postedData    = "";

    function postData(chunk)
    {
        console.log("Received POST data chunk '" + chunk + "'");
        postedData += chunk;
    }

    function postEnd()
    {
        route(handle, request, pathname, query, postedData, response);
    }

    request.setEncoding("utf8");
    request.addListener("data", postData);
    request.addListener("end",  postEnd);
}

function serveStaticFile(request, pathname, response)
{
    // Serve library files under "<server>/lib/"
    var pathDirs     = pathname.split("/");
    var content_type = "";

    // pathDirs[0] will be the empty string before the first "/"
    if(pathDirs.length < 3)
        return false;

    if(pathDirs[1] == "html")
        content_type = "text/html";
    else if(pathDirs[1] == "js" || pathDirs[1] == "lib")
        content_type = "text/javascript";
    else if(pathDirs[1] == "data")
        content_type = "application/octet-stream";
    else
        return false;
       
    var pagePath = path.join(__dirname, '../client', pathname);
    console.log("Attempting to serve page: " + pagePath);

    response.writeHead(200, {"Content-Type": content_type});
    var input = fs.createReadStream(pagePath);
    input.on("data", function(data) { response.write(data); });

    input.on("error", function(err) { 
        console.log("Error reading static file"); 
        response.writeHead(404, {"Content-Type": "text/plain"});
        response.end("File not found"); });

    input.on("end", function() { response.end(); });

    return true;
}

exports.start = start;

