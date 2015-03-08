#!/usr/bin/env python

import matplotlib.pyplot as plt
from numpy import log2
from scipy import arange
#from mpl_toolkits.mplot3d import Axes3D

from dspUtils import get_fft


def plot_log_spectrum(y, Fs, upper_frequency=0):
    """
    plot spectrum on a log-frequency scale
    """
    frq, ampl = get_fft(y, Fs, upper_frequency)
    log_frq = log2(frq[1:])  # don't take log(0)
    display_ampl = log2(ampl[1:])
    plt.plot(log_frq, display_ampl, 'r')    # plotting the spectrum
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')

# in progress...
def plot_smooth_log_spectrum(y, Fs, upper_frequency=0):
    """
    plot spectrum on a log-frequency scale, then convolve with a gaussian filter
    """
    frq, ampl = get_fft(y, Fs, upper_frequency)
    log_frq = log2(frq[1:])  # don't take log(0)
    log_ampl = log2(ampl[1:])

    # Smooth the amplitude
    # gauss_filter = scipy.signal.gaussian(

    plt.plot(log_frq, log_ampl, 'r')    # plotting the spectrum
    plt.xlabel('Log Freq (Hz)')
    plt.ylabel('|Y(freq)|')

def plot_spectrum(y, Fs, upper_frequency=0):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    frq, ampl = get_fft(y, Fs, upper_frequency)
    plt.plot(frq, ampl, 'r') # plotting the spectrum
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')

def plot_wave(y, Fs):
    """
    Plots waveform y having sample frequency Fs
    """
    n = len(y)
    T = n/Fs
    t = arange(0, T, 1.0/Fs)
    plt.plot(t, y)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

def plot_samples_3d(samples, labels):
    """
    Plot a 3D collection of histograms with different colors for different labels.
    Most effective if the samples for a given label occur together.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = np.arange(len(samples[0]))
    label_color_map = get_label_color_map(labels)

    for index in range(len(samples)):
        ys = np.array(samples[index])
        label_color = label_color_map[labels[index]]
        ax.bar(xs, ys, zs=index, zdir='y', color=label_color, alpha=0.7)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
