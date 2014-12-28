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

        serveJsonRequest(route, handle, request, response);
    }

    var server = http.createServer(onRequest);
    server.listen(config.server_port); 
    console.log('Server running on port ' + config.server_port);
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

