#!/usr/bin/env python

import argparse
import scipy

from numpy import sin, linspace, pi, log2
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange
from scipy.io.wavfile import read

def getFFT(y, Fs, freq_limit=0):
    """
    Computes a Single-Sided Amplitude Spectrum of y(t), and returns freq, amplitude
    """
    n = len(y)            # length of the signal
    max_freq = Fs/2
    max_index = n/2

    if(freq_limit > 0 and freq_limit < max_freq):
        # Scale the index for the desired freq_limit: max_index * (freq_limit/max_freq)
        max_index = int(max_index * float(freq_limit)/max_freq)

    k = arange(n)         # sample indices
    T = float(n)/Fs       # duration of signal
    frq = k/T             # two sides frequency range (0..#samples/#seconds)
    frq = frq[:max_index] # one side frequency range

    Y = fft(y)/n          # fft computing and normalization
    Y = Y[:max_index]
    return frq, abs(Y)

def plotLogSpectrum(y, Fs, freq_limit=0):
    """
    plot spectrum on a log-frequency scale
    """
    frq, ampl = getFFT(y, Fs, freq_limit)
    log_frq = log2(frq[1:])  # don't take log(0)
    display_ampl = log2(ampl[1:])
    plot(log_frq, display_ampl, 'r')    # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

def plotSmoothLogSpectrum(y, Fs, freq_limit=0):
    """
    plot spectrum on a log-frequency scale, then convolve with a gaussian filter
    """
    frq, ampl = getFFT(y, Fs, freq_limit)
    log_frq = log2(frq[1:])  # don't take log(0)
    log_ampl = log2(ampl[1:])

    # Smooth the amplitude
    # gauss_filter = scipy.signal.gaussian(

    plot(log_frq, log_ampl, 'r')    # plotting the spectrum
    xlabel('Log Freq (Hz)')
    ylabel('|Y(freq)|')

def plotSpectrum(y,Fs, freq_limit=0):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y)            # length of the signal
    max_freq = Fs/2
    max_index = n/2

    if(freq_limit > 0 and freq_limit < max_freq):
        # Scale the index for the desired freq_limit: max_index * (freq_limit/max_freq)
        max_index = int(max_index * float(freq_limit)/max_freq)

    k = arange(n)         # sample indices
    T = float(n)/Fs       # duration of signal
    frq = k/T             # two sides frequency range (0..#samples/#seconds)
    frq = frq[:max_index] # one side frequency range

    Y = fft(y)/n # fft computing and normalization
    Y = Y[:max_index]

    plot(frq, abs(Y), 'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

def plotWave(y, Fs):
    """
    Plots waveform y having sample frequency Fs
    """
    n = len(y)
    T = n/Fs
    t = arange(0, T, 1.0/Fs)
    plot(t, y)
    xlabel('Time')
    ylabel('Amplitude')

def displayWaveAndSpectrum(y, Fs, freq_limit=0):
    subplot(2,1,1)      # multiple plots: 2 rows, 1 column, 1st plot
    plotLogSpectrum(y, Fs)
    subplot(2,1,2)      # ... second plot
    plotSpectrum(y,Fs, freq_limit)
    show()

def test():
    Fs = 150.0;  # sampling rate
    Ts = 1.0/Fs; # sampling interval
    t = arange(0,1,Ts) # time vector

    ff = 5;   # frequency of the signal
    y = sin(2*pi*ff*t)

    displayWaveAndSpectrum(y, Fs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start",
                        help="index of first sample file to plot")

    parser.add_argument("count",
                        help="number of successive sample_NNN.wav input files")

    parser.add_argument("freq_limit",
                        help="highest frequency to plot")

    args = parser.parse_args()
    start = int(args.start)
    count = int(args.count)
    freq_limit = int(args.freq_limit)

    for i in range(count):
        subplot(count, 1, i+1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        Fs, data = read(wav_filename)
        plotSpectrum(data, Fs, freq_limit)
    show()

    
if __name__ == "__main__":
    #test()
    main()

