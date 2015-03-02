#!/usr/bin/env python

import os
import glob
import argparse
import matplotlib.pyplot as plt
from pylab import show, subplot
from scipy.io.wavfile import read

from plotUtils import plot_spectrum

DEFAULT_NUMBER_SAMPLES = 5


def plot_series(folder_prefix, start=0, number_samples=DEFAULT_NUMBER_SAMPLES, upper_frequency=0):
    plt.rcParams['figure.figsize'] = (24.0, 16.0)
    plt.axis("off")

    # Allow the folder prefix, e.g., "Samples_000" to suffice in specifying the folder
    folder_matches = glob.glob(folder_prefix + '*')
    if len(folder_matches) >= 1:
        folder = folder_matches[0]
    else:
        print "Failed to find sample folder with prefix {}".format(folder_prefix)
        return

    for i in range(number_samples):
        plt.subplot(number_samples, 1, i + 1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        wav_path = os.path.join(folder, wav_filename)
        Fs, data = read(wav_path)
        plot_spectrum(data, Fs, upper_frequency)

    plt.suptitle(folder)
    show()

def main():
    parser = argparse.ArgumentParser(
        description="Plot a series of .wav files from the specified folder.")
    parser.add_argument("folder",
                        help="path to folder containing sample files")

    parser.add_argument("-n", "--number_samples", type=int,
                        default=DEFAULT_NUMBER_SAMPLES,
                        help="Number of samples (default {})".format(DEFAULT_NUMBER_SAMPLES))

    parser.add_argument("-s", "--start", type=int,
                        default=0,
                        help="First sample index (default 0)")

    parser.add_argument("-l", "--lower_frequency",
                        default=0,
                        help="Lowest frequency to plot (default 0)")

    parser.add_argument("-u", "--upper_frequency",
                        default=0,
                        help="Highest frequency to plot (default is all available)")

    args = parser.parse_args()
    start = int(args.start)
    number_samples = int(args.number_samples)
    upper_frequency = int(args.upper_frequency)

    plot_series(args.folder, start, number_samples, upper_frequency)

if __name__ == "__main__":
    main()
