function playWaveFile()
{
    wavesurfer.play();
}

function loadWave(jqueryWaveName, jqueryWaveContainer, wave_path)
{
    var wavesurfer = Object.create(WaveSurfer);

    wavesurfer.init({
        container: jqueryWaveContainer[0],
        waveColor: '#00F0F0',
        progressColor: '#00A0A0',
        //waveColor: 'violet',
        //progressColor: 'purple',
        cursorWidth: 0
    });
    
    wavesurfer.load(wave_path);
    jqueryWaveName.click(function() { wavesurfer.play(); });
}

function mainLoop()
{
    var waveList = $("#waveList");
    var waveTable = $("<table style='width:100%'/>", { "border" : 1 }).appendTo(waveList);

    // Retrieve list of sample filenames.
    $.get("/sample_list", function(sample_list,status){
        for(var i = 0; i < sample_list.length; i++) {
            var sampleName = sample_list[i];

            // For each filename, create a table entry and load a WaveSurfer object
            var row = $("<tr>").appendTo(waveTable);
            var col1 = $("<td style='width:10%'>").text(sampleName).appendTo(row);
            var sampleId = "wave" + i;
            var col2 = $("<td>").attr("id", sampleId).appendTo(row);

            console.log(sampleId);
            loadWave(col1, col2, '/data/' + sampleName);
        }
    });
}

$(document).ready(mainLoop);
