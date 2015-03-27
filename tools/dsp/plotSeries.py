#!/usr/bin/env python

import os
import glob
import argparse
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from pylab import show, subplot
from scipy.io.wavfile import read

from plotUtils import plot_spectrum, plot_correlation, plot_wave
import dspUtils

DEFAULT_NUMBER_SAMPLES = 5


def get_folder(folder_prefix):
    # Allow the folder prefix, e.g., "Samples_000" to suffice in specifying the folder
    folder_matches = glob.glob(folder_prefix + '*')
    if len(folder_matches) >= 1:
        return folder_matches[0]
    else:
        print "Failed to find sample folder with prefix {}".format(folder_prefix)
        return ""


def get_dataset_avg_fft(dataset_path, upper_frequency=0):
    ds_folder = get_folder(dataset_path)
    if not ds_folder:
        return

    # Create list of all Samples folders
    sample_folder_prefix = os.path.join(ds_folder, "Samples_")
    sample_folders = glob.glob(sample_folder_prefix + '*')
    #print "Found {} folders".format(len(sample_folders))

    sample_count = 0
    frq = []
    total_ampl = []
    for folder in sample_folders:
        sample_prefix = os.path.join(folder, "sample_")
        samples = glob.glob(sample_prefix + '*')

        for sample in samples:
            Fs, data = sp.io.wavfile.read(sample)
            frq, ampl = dspUtils.get_fft(data, Fs, upper_frequency)

            # Kludgy, but avoids figuring out size of the ampl array before we load the first one
            if len(total_ampl) == 0:
                total_ampl = ampl
            else:
                total_ampl += ampl
            sample_count += 1

    avg_ampl = total_ampl / sample_count
    return frq, avg_ampl # Assume all frq arrays are identical; return the last one


def get_dataset_avgs(dataset_path, upper_frequency=0):
    """Create an array with the average fft for each sample folder"""
    ds_folder = get_folder(dataset_path)
    if not ds_folder:
        return

    # Create list of all Samples folders
    sample_folder_prefix = os.path.join(ds_folder, "Samples_")
    sample_folders = glob.glob(sample_folder_prefix + '*')
    #print "Found {} folders".format(len(sample_folders))

    sample_set_avgs = []
    for folder in sample_folders:
        sample_prefix = os.path.join(folder, "sample_")
        samples = glob.glob(sample_prefix + '*')

        sample_count = 0
        frq = []
        total_ampl = np.array([])
        for sample in samples:
            Fs, data = sp.io.wavfile.read(sample)
            frq, ampl = dspUtils.get_fft(data, Fs, upper_frequency)

            # Kludgy, but avoids figuring out size of the ampl array before we load the first one
            if len(total_ampl) == 0:
                total_ampl = ampl
            else:
                total_ampl += ampl
            sample_count += 1

        # Assume all frq arrays are identical for a dataset; use the last one
        sample_set_avgs.append((frq, total_ampl / sample_count))

    # Total the ffts across the entire dataset
    if len(sample_set_avgs):
        dataset_frq = sample_set_avgs[0][0]
        dataset_ampl = np.zeros(len(dataset_frq))
        for frq, ampl in sample_set_avgs:
            dataset_ampl += ampl
        return sample_set_avgs, dataset_frq, dataset_ampl/len(sample_set_avgs)
    else:
        print "Empty dataset!"
        return [], [], []


def plot_dataset_avg(dataset_path, upper_frequency=0):
    frq, avg_ampl = get_dataset_avg_fft(dataset_path, upper_frequency)
    plt.plot(frq, avg_ampl, 'r')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Avg Ampl|')
    plt.show()


def plot_series_fft(folder_prefix, start=0, number_samples=DEFAULT_NUMBER_SAMPLES, upper_frequency=0):
    plt.rcParams['figure.figsize'] = (24.0, 16.0)
    plt.axis("off")

    folder = get_folder(folder_prefix)
    if not folder:
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


def plot_series_correlation(folder_prefix, start=0, number_samples=DEFAULT_NUMBER_SAMPLES, max_overlap_sec=1.0):
    plt.rcParams['figure.figsize'] = (24.0, 16.0)
    plt.axis("off")

    folder = get_folder(folder_prefix)
    if not folder:
        return

    for i in range(number_samples):
        plt.subplot(number_samples, 1, i + 1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        wav_path = os.path.join(folder, wav_filename)
        Fs, data = read(wav_path)
        plot_correlation(data, Fs, max_overlap_sec)

    plt.suptitle(folder)
    show()


def plot_series_function(plot_function, folder_prefix, start=0, number_samples=DEFAULT_NUMBER_SAMPLES):
    plt.rcParams['figure.figsize'] = (24.0, 16.0)
    plt.axis("off")

    folder = get_folder(folder_prefix)
    if not folder:
        return

    for i in range(number_samples):
        plt.subplot(number_samples, 1, i + 1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        wav_path = os.path.join(folder, wav_filename)
        Fs, data = read(wav_path)
        plot_function(data, Fs)

    plt.suptitle(folder)
    show()


def plot_series_wave(folder_prefix, start=0, number_samples=DEFAULT_NUMBER_SAMPLES, start_sec=0, stop_sec=0):
    plotter = lambda data, Fs: plot_wave(data, Fs, start_sec, stop_sec)
    plot_series_function(plotter, folder_prefix, start, number_samples)


def plot_smoothed_samples(folder_prefix, start=0, number_samples=1, upper_frequency=0, kernel_length=11):
    """Apply successive smoothing filters to the sample and plot the result"""
    folder = get_folder(folder_prefix)
    if not folder:
        return

    for i in range(number_samples):
        plt.subplot(2*number_samples, 1, 2*i + 1)
        index = start + i
        wav_filename = "sample_{}.wav".format(str(index).zfill(3))
        wav_path = os.path.join(folder, wav_filename)
        Fs, data = read(wav_path)
        plot_spectrum(data, Fs, upper_frequency)

        plt.subplot(2*number_samples, 1, 2*i + 2)
        frq, ampl = dspUtils.get_fft(data, Fs, upper_frequency)
        smoothed_sample = dspUtils.smooth_with_gaussian_kernel(ampl, kernel_length)
        plt.plot(frq, smoothed_sample, 'b') # plotting the spectrum
        plt.xlabel('Freq (Hz)')
        plt.ylabel('|Y(freq)|')

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
