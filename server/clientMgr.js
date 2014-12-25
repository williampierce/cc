// Manage the socket.io interface with all clients

// Set of all socket connections
g_activeSockets = {};

function register(socket)
{
    console.log("Client connect, registering socket, ID = " + socket.id);

    g_activeSockets[socket.id] = socket;
}

function deRegister(socket)
{
    console.log("Client disconnect, deregistering socket, ID = " + socket.id);

    // Insert socket.id in the set of active sockets
    delete g_activeSockets[socket.id];
}

// Note, we can use io.emit to send data to all sockets at once, but we'll do it
// explicitly here, since in general we may treat clients differently.
function broadcastState(networkState)
{
    // var jsonState = JSON.stringify(networkState);

    for(socketId in g_activeSockets)
    {
        g_activeSockets[socketId].emit("date", {"date": new Date()});
        g_activeSockets[socketId].emit("networkState", networkState);
    }
}

exports.register       = register;
exports.deRegister     = deRegister;
exports.broadcastState = broadcastState;
