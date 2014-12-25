function route(handle, request, pathname, query, postData, response) 
{
    if (typeof handle[pathname] === 'function') 
    {
        handle[pathname](request, query, postData, response);
    } 
    else
    {
        console.log("No request handler found for " + pathname);
        response.writeHead(404, {"Content-Type": "text/plain"});
        response.write("404 Not found");
        response.end();
    }
}

exports.route = route;
