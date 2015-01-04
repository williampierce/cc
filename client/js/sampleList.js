// Create and return a WaveSurfer object
function loadWave(jqueryWaveName, jqueryWaveContainer, wave_path)
{
    var wavesurfer = Object.create(WaveSurfer);

    wavesurfer.on('error', function (error) {
        console.log('WaveSurfer error event: ' + error);
    });
    wavesurfer.init({
        container: jqueryWaveContainer[0],
        waveColor: '#00F0F0',
        progressColor: '#00A0A0',
        cursorWidth: 0
    });
    wavesurfer.load(wave_path);

    jqueryWaveName.click(function() { 
        try {
            wavesurfer.play();
        }
        catch(error) {
            console.log('WaveSurfer.play() caught error: ' + error);
        }
    });

    return wavesurfer;
}

var prevSampleList = {};
var activeWavesurfers = [];

function mainLoop()
{
    // Retrieve list of sample filenames.
    $.get("/sample_list")
        .done(function(sampleList, status) {
            var sampleListStr = JSON.stringify(sampleList);

            if(!_.isEqual(sampleList, prevSampleList)) {
                prevSampleList = sampleList;

                var waveList = $("#waveList").html("");
                var waveTable = $("<table style='width:100%'/>", { "border" : 1 }).appendTo(waveList);

                // Destroy any previous wavesurfer objects
                while(activeWavesurfers.length) {
                    activeWavesurfers.pop().destroy();
                }

                for(var i = 0; i < sampleList.length; i++) {
                    var sampleName = sampleList[i];

                    // For each filename, create a table entry and load a WaveSurfer object
                    var row = $("<tr>").appendTo(waveTable);
                    var col1 = $("<td style='width:10%'>").text(sampleName).appendTo(row);
                    var sampleId = "wave" + i;
                    var col2 = $("<td>").attr("id", sampleId).appendTo(row);

                    var wavesurfer = loadWave(col1, col2, '/data/' + sampleName);
                    activeWavesurfers.push(wavesurfer);
                }
            }
        }).always(function() {
            setTimeout(mainLoop, 5000);
        });
}

$(document).ready(mainLoop);
