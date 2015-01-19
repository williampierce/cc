#!/usr/bin/env python

from scipy import fft, arange

def getFFT(y, Fs, upper_frequency=0):
    """
    Computes a Single-Sided Amplitude Spectrum of y(t), and returns freq, amplitude
    """
    n = len(y)            # length of the signal
    max_freq = Fs/2
    max_index = n/2

    if(upper_frequency > 0 and upper_frequency < max_freq):
        # Scale the index for the desired upper_frequency: max_index * (upper_frequency/max_freq)
        max_index = int(max_index * float(upper_frequency)/max_freq)

    k = arange(n)         # sample indices
    T = float(n)/Fs       # duration of signal
    frq = k/T             # two sides frequency range (0..#samples/#seconds)
    frq = frq[:max_index] # one side frequency range

    Y = fft(y)/n          # fft computing and normalization
    Y = Y[:max_index]
    return frq, abs(Y)

