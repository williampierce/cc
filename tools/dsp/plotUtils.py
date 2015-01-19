#!/usr/bin/env python

import matplotlib.pyplot as plt
from numpy import log2
from scipy import arange

from dspUtils import getFFT


def plotLogSpectrum(y, Fs, upper_frequency=0):
    """
    plot spectrum on a log-frequency scale
    """
    frq, ampl = getFFT(y, Fs, upper_frequency)
    log_frq = log2(frq[1:])  # don't take log(0)
    display_ampl = log2(ampl[1:])
    plt.plot(log_frq, display_ampl, 'r')    # plotting the spectrum
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')

# in progress...
def plotSmoothLogSpectrum(y, Fs, upper_frequency=0):
    """
    plot spectrum on a log-frequency scale, then convolve with a gaussian filter
    """
    frq, ampl = getFFT(y, Fs, upper_frequency)
    log_frq = log2(frq[1:])  # don't take log(0)
    log_ampl = log2(ampl[1:])

    # Smooth the amplitude
    # gauss_filter = scipy.signal.gaussian(

    plt.plot(log_frq, log_ampl, 'r')    # plotting the spectrum
    plt.xlabel('Log Freq (Hz)')
    plt.ylabel('|Y(freq)|')

def plotSpectrum(y, Fs, upper_frequency=0):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    frq, ampl = getFFT(y, Fs, upper_frequency)
    plt.plot(frq, ampl, 'r') # plotting the spectrum
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')

def plotWave(y, Fs):
    """
    Plots waveform y having sample frequency Fs
    """
    n = len(y)
    T = n/Fs
    t = arange(0, T, 1.0/Fs)
    plt.plot(t, y)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

