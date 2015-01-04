function loadWave(jqueryWaveName, jqueryWaveContainer, wave_path)
{
    var wavesurfer = Object.create(WaveSurfer);

    wavesurfer.init({
        container: jqueryWaveContainer[0],
        waveColor: '#00F0F0',
        progressColor: '#00A0A0',
        cursorWidth: 0
    });
    
    wavesurfer.load(wave_path);
    jqueryWaveName.click(function() { wavesurfer.play(); });
}

var prevSampleList = {};

function mainLoop()
{
    // Retrieve list of sample filenames.
    $.get("/sample_list")
        .done(function(sampleList, status) {
            var sampleListStr = JSON.stringify(sampleList);

            if(!_.isEqual(sampleList, prevSampleList)) {
                console.log(sampleList);
                prevSampleList = sampleList;

                var waveList = $("#waveList").html("");
                var waveTable = $("<table style='width:100%'/>", { "border" : 1 }).appendTo(waveList);

                for(var i = 0; i < sampleList.length; i++) {
                    var sampleName = sampleList[i];

                    // For each filename, create a table entry and load a WaveSurfer object
                    var row = $("<tr>").appendTo(waveTable);
                    var col1 = $("<td style='width:10%'>").text(sampleName).appendTo(row);
                    var sampleId = "wave" + i;
                    var col2 = $("<td>").attr("id", sampleId).appendTo(row);

                    console.log(sampleId);
                    loadWave(col1, col2, '/data/' + sampleName);
                }
            }
        }).always(function() {
            setTimeout(mainLoop, 5000);
        });
}

$(document).ready(mainLoop);
