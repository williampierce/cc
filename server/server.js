var http      = require('http');
var url       = require('url');
var fs        = require('fs');
var path      = require('path');
var clientMgr = require('./clientMgr');

var g_serverPort = 8765;

// Given a routing function and a mapping from pathnames to request handlers, this
// function will create a server to handle http requests on port g_serverPort.
// If a pathname has the form "/static/<page>", then the specified page will be
// delivered and no handler will be called.
function start(route, handle)
{
    function onRequest(request, response)
    {
        var request_parse = url.parse(request.url);
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
            // End of posted data
            // If the request is for a static or library page, return it; otherwise, route the request
            if(serveStaticPage(request, pathname, response))
                return;
            if(serveStaticFile(request, pathname, response))
                return;
            route(handle, request, pathname, query, postedData, response);
        }

        console.log("HTTP " + request.method + " request for " + pathname + " received");
        if(query)
            console.log("  Query: " + query);

        request.setEncoding("utf8");
        request.addListener("data", postData);
        request.addListener("end",  postEnd);
    }

    var server = http.createServer(onRequest);
    server.listen(g_serverPort); 

    // Set up socket.io
    var io = require('socket.io')(server);

    io.on("connect", function(socket){
        socket.emit("ack", "Welcome, socket number " + socket.id + " !");

        // Register the socket with the client manager
        clientMgr.register(socket);

        // Send the date every second
        /*
        setInterval(function(){
            clientMgr.broadcastState({});
            // socket.emit("date", {"date": new Date()});
        }, 1000);
        */

        // Capture client events
        socket.on("client_data", function(data){
            process.stdout.write(data.letter);
        });

        socket.on("disconnect", function(){
            clientMgr.deRegister(socket);
        });
    });

    console.log('Server running on port ' + g_serverPort);
}

// This doesn't currently handle nesting of static files
function serveStaticPage(request, pathname, response)
{
    // Allow a special case to play with static pages
    var pathDirs = pathname.split("/");

    // pathDirs[0] will be the empty string before the first "/"
    if(pathDirs[1] == "static" && pathDirs.length == 3)
    {
        var pagePath = path.join(__dirname, "static", pathDirs[2]);
        // console.log("Attempting to serve page: " + pagePath);

        var input = fs.createReadStream(pagePath);
        input.on("data", function(data) { response.write(data); });

        input.on("error", function(err) { 
                console.log("Error reading static file"); 
                response.writeHead(404, {"Content-Type": "text/plain"});
                response.end("File not found"); });

        input.on("end", function() { response.end(); });

        return true;
    }
    return false;
}

function serveStaticFile(request, pathname, response)
{
    // Serve library files under "<server>/lib/"
    var pathDirs = pathname.split("/");

    // pathDirs[0] will be the empty string before the first "/"
    if((pathDirs[1] == "html" || pathDirs[1] == "src" || pathDirs[1] == "lib" || pathDirs[1] == "data") && pathDirs.length >= 3)
    {
        var pagePath = __dirname.concat(pathname);
        console.log("Attempting to serve page: " + pagePath);

        response.writeHead(200, {"Content-Type": "text/javascript"});
        var input = fs.createReadStream(pagePath);
        input.on("data", function(data) { response.write(data); });

        input.on("error", function(err) { 
                console.log("Error reading static file"); 
                response.writeHead(404, {"Content-Type": "text/plain"});
                response.end("File not found"); });

        input.on("end", function() { response.end(); });

        return true;
    }
    return false;
}

exports.start = start;

