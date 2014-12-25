// Contains the business logic. Maintains state based on inputs; updates device state.
//
// In the initial design, the operator does not control the devices. The state of each device
// is determined by the rules captured here, and the operator's dashboard just provides the
// state of the devices.

var deviceControl = require("./deviceControl");
var clientMgr     = require("./clientMgr");

// Current state of all devices
//     Map: agentId -> {timeStamp: <time>, face : 1..6}
var g_agentState = {};

// Current agents voting for each face
//     Map: face -> set of agents selecting that face
//     We use 0 for the undetermined face.
var g_faceToAgentMap = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}};

// Current majority face
var g_majorityFace = 0;


// getNetworkState()
//     { majorityFace: <int>,
//       numDevices: <int>,
//       agentStates: g_agentState,
//       faceToAgentMap: g_faceToAgentMap,
//     }
function getNetworkState()
{
    var networkState = {};

    networkState.majorityFace   = g_majorityFace;
    networkState.numDevices     = g_agentState.length;
    networkState.agentState     = g_agentState;
    networkState.faceToAgentMap = g_faceToAgentMap;

    return networkState;
}

function updateState(state)
{
    // state: {agentId : <agent id string>, face : 0..6}

    console.log("Updating state for request: " + JSON.stringify(state));

    var agentId  = state.agentId;
    var timeStamp = (new Date()).getTime();


    // 1. Update the entry for this agent. If the face has changed, update the face agent lists.
    var oldFace = (agentId in g_agentState) ? g_agentState[agentId].face : 0;
    var newFace = state.face;

    // Force newFace to a valid value
    var validFaces = {0:true, 1:true, 2:true, 3:true, 4:true, 5:true, 6:true};
    if(!(newFace in validFaces))
        newFace = 0;

    if(!(agentId in g_agentState)){
        // New agent: create a new state entry
        console.log("Creating new agent entry for " + agentId + ": face=" + newFace);
        g_agentState[agentId] = {};
        g_agentState[agentId].face = newFace;

        // Add this agent to the appropriate face map
        g_faceToAgentMap[newFace][agentId] = true;
    }

    var oldFace = g_agentState[agentId].face;

    if(newFace != oldFace)
    {
        // Existing and modified agent: update the agent entry
        console.log("Updating face for agent " + agentId + ": " + oldFace + "->" + newFace);
        g_agentState[agentId].face = newFace;

        // Move this agent from the previous to the new face map
        delete g_faceToAgentMap[oldFace][agentId]; // remove from old map
        g_faceToAgentMap[newFace][agentId] = true; // add to new map
    }

    // Record the timestamp for this update
    g_agentState[agentId].timeStamp = timeStamp;


    // 2. Compute the majority face
    var majorityFace = getMajorityFace();
 
    // 3. Update all devices if majority face has changed
    if(majorityFace != g_majorityFace)

    {
        g_majorityFace = majorityFace;

        // Set the majorityFace for each agent
        for(agentId in g_agentState)
        {
            var state = { "agentId" : agentId, "face" : g_majorityFace};
            deviceControl.setState(state);
        }
    }

    // 4. Always update the client dashboard
    var networkState = {
        "majority"       : g_majorityFace,
        "faceToAgentMap" : g_faceToAgentMap
    };
    clientMgr.broadcastState(networkState);
}

// Ties will go to the lower numbered face
function getMajorityFace()
{
    var faceCounts = [0, 0, 0, 0, 0, 0, 0]; // counts for 0..6

    for(agentId in g_agentState)
        faceCounts[g_agentState[agentId].face]++;

    var maxCount = 0;
    var maxFace  = 0;

    for(var i=0; i<faceCounts.length; i++)
    {
        if(faceCounts[i] > maxCount)
        {
            maxCount = faceCounts[i];
            maxFace  = i;
        }
    }
    console.log("    Current face counts:   " + faceCounts);
    console.log("    Current majority face: " + maxFace);

    return maxFace;
}

exports.getNetworkState = getNetworkState;
exports.updateState     = updateState;

