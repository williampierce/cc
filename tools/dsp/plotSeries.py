#!/usr/bin/env python

import os
import argparse
import matplotlib.pyplot as plt
from pylab import show, subplot
from scipy.io.wavfile import read

from plotUtils import plotSpectrum

DEFAULT_NUMBER_SAMPLES = 5

def main():
    parser = argparse.ArgumentParser(
        description = "Plot a series of .wav files from the specified folder.")
    parser.add_argument("folder",
                        help="path to folder containing sample files")

    parser.add_argument("-n", "--number_samples", type=int,
                        default=DEFAULT_NUMBER_SAMPLES,
                        help="Number of samples (default {})".format(DEFAULT_NUMBER_SAMPLES))

    parser.add_argument("-s", "--start", type=int,
                        default = 0,
                        help="First sample index (default 0)")

    parser.add_argument("-l", "--lower_frequency",
                        default = 0,
                        help="Lowest frequency to plot (default 0)")

    parser.add_argument("-u", "--upper_frequency",
                        default = 0,
                        help="Highest frequency to plot (default is all available)")

    args = parser.parse_args()
    start = int(args.start)
    number_samples = int(args.number_samples)
    upper_frequency = int(args.upper_frequency)

    plt.axis("off")

    for i in range(number_samples):
        plt.subplot(number_samples, 1, i+1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        wav_path = os.path.join(args.folder, wav_filename)
        Fs, data = read(wav_path)
        plotSpectrum(data, Fs, upper_frequency)

    plt.suptitle(args.folder)
    show()

    
if __name__ == "__main__":
    main()

