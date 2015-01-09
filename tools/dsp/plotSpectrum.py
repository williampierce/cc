#!/usr/bin/env python

import argparse
import scipy

from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange
from scipy.io.wavfile import read

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
    plotWave(y, Fs)
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
    parser.add_argument("input",
                        help=".wav input file")

    parser.add_argument("freq_limit",
                        help="highest frequency to plot")

    args         = parser.parse_args()
    wav_filename = args.input
    freq_limit   = args.freq_limit
    dat_filename = ""

    print "input: " + wav_filename + ", freq_limit: " + freq_limit
    Fs, data = read(wav_filename)
    displayWaveAndSpectrum(data, Fs, int(freq_limit))
    
if __name__ == "__main__":
    #test()
    main()

