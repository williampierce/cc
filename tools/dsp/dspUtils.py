#!/usr/bin/env python

from scipy import fft, arange

def get_fft(y, Fs, upper_frequency=0):
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

'''
def get_histogram(y_values, number_bins):
    # Partition the y_values evenly
    number_entries = len(y_values)
    histogram = []
    total_sum = 0
    min_bin_index = 0
    for bin_count in range(1, number_bins+1):
        max_bin_index = number_entries * bin_count / number_bins
        bin_sum = sum(y_values[min_bin_index:max_bin_index])
        histogram.append(bin_sum)
        total_sum += bin_sum
        min_bin_index = max_bin_index

    return histogram/total_sum
'''
