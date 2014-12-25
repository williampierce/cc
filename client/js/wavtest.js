var wavesurfer = Object.create(WaveSurfer);

wavesurfer.init({
    container: document.querySelector('#wave'),
    waveColor: 'violet',
    progressColor: 'purple'
});

//wavesurfer.on('ready', function () {
//    wavesurfer.play();
//});

function playWaveFile()
{
    wavesurfer.play();
}

wavesurfer.load('/data/wav_files/Side_Left.wav');
