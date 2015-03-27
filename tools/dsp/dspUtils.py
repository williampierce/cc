#!/usr/bin/env python

import numpy as np
import scipy as sp


def get_fft(y, Fs, upper_frequency=0):
    """
    Computes a single-sided amplitude spectrum of y(t), and returns freq, amplitude
    """
    N = len(y)  # length of the signal
    max_freq = Fs / 2
    nfreqs = N / 2

    if 0 < upper_frequency < max_freq:
        # Scale the index for the desired upper_frequency: nfreqs * (upper_frequency/max_freq)
        nfreqs = int(nfreqs * float(upper_frequency) / max_freq)
        max_freq = upper_frequency

    xf = np.linspace(0.0, max_freq, nfreqs)

    # Compute fft; limit to selected, positive frequencies, normalize
    # Double the amplitude to account for energy from symmetric, negative spectrum
    # Apply a hanning window before computing the DFT to reduce spectral leakage
    hw = sp.hanning(N)
    yf = 2.0/N * abs(sp.fft(y*hw)[:nfreqs])

    return xf, yf


def gaussian_kernel_1d(length=11, nsigma=3):
    """
    Create a 1d gaussian kernel spanning nsigma std devs on each side.
    If length is even, returns kernel of width length+1
    """
    n = int(length) / 2
    xrange = range(-n, n + 1)
    sigma = float(n) / nsigma
    return [1 / (sigma * np.math.sqrt(2 * np.math.pi)) * np.math.exp(-float(x) ** 2 / (2 * sigma ** 2)) for x in xrange]


def smooth_with_gaussian_kernel(signal, kernel_width):
    """Smooth univariate signal with gaussian kernel"""
    kernel = gaussian_kernel_1d(kernel_width)
    smoothed_signal = sp.convolve(signal, kernel, 'same')
    return smoothed_signal
