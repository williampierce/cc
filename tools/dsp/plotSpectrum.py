#!/usr/bin/env python

import argparse
from pylab import show, subplot
from scipy.io.wavfile import read

from plotUtils import plot_spectrum, plot_log_spectrum

def display_wave_and_spectrum(y, Fs, freq_limit=0):
    subplot(2,1,1)      # multiple plots: 2 rows, 1 column, 1st plot
    plot_log_spectrum(y, Fs)
    subplot(2,1,2)      # ... second plot
    plot_spectrum(y,Fs, freq_limit)
    show()

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
    display_wave_and_spectrum(data, Fs, int(freq_limit))
    
if __name__ == "__main__":
    main()

