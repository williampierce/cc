function playWaveFile()
{
    wavesurfer.play();
}

function loadWave(container, wave_path)
{
    var wavesurfer = Object.create(WaveSurfer);

    wavesurfer.init({
        //container: document.querySelector(container_id),
        container: container,
        waveColor: 'violet',
        progressColor: 'purple',
        cursorWidth: 0
    });
    
    wavesurfer.load(wave_path);
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
            loadWave(col2[0], '/data/wav_files/Side_Left.wav');
        }
    });
}

$(document).ready(mainLoop);
