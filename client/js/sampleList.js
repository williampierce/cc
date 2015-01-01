var wavesurfer = Object.create(WaveSurfer);

wavesurfer.init({
    container: document.querySelector('#wave'),
    waveColor: 'violet',
    progressColor: 'purple'
});

function playWaveFile()
{
    wavesurfer.play();
}

wavesurfer.load('/data/wav_files/Side_Left.wav');

function mainLoop()
{
    // Retrieve list of sample filenames.
    //$("#waveList").load('/sample_list');

    $.get("/sample_list", function(sample_list,status){
        //$("#waveList").load(sample_list);
        for(var i = 0; i < sample_list.length; i++) {
            $("#waveList").append(sample_list[i]);
        }
    });
}

$(document).ready(mainLoop);
