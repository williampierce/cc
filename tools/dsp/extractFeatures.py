#!/usr/bin/env python

import argparse
import os
import glob
import re
import numpy as np
from scipy.io.wavfile import read

from dspUtils import getFFT

DEFAULT_NUMBER_SAMPLES = 5
DEFAULT_NUMBER_BINS = 8

def GetHistogram(y_values, number_bins):
    # Partition the y_values evenly
    number_entries = len(y_values)
    histogram = []
    min_bin_index = 0
    for bin_count in range(1, number_bins+1):
        max_bin_index = number_entries * bin_count / number_bins
        histogram.append(sum(y_values[min_bin_index:max_bin_index]))
        min_bin_index = max_bin_index

    return histogram

def main():
    parser = argparse.ArgumentParser(
        description = "Create a feature set array and a corresponding label array from the 'Sample_NNN' subfolders.")
    parser.add_argument("dataset",
                        help="path to dataset folder containing samples folders")

    parser.add_argument("-n", "--number_samples", type=int,
                        default=DEFAULT_NUMBER_SAMPLES,
                        help="Number of samples (default {})".format(DEFAULT_NUMBER_SAMPLES))

    parser.add_argument("-b", "--number_bins", type=int,
                        default=DEFAULT_NUMBER_BINS,
                        help="Number of bins (default {})".format(DEFAULT_NUMBER_BINS))

    parser.add_argument("-s", "--start", type=int,
                        default = 0,
                        help="First sample index (default 0)")

    parser.add_argument("-l", "--lower_frequency",
                        default = 0,
                        help="Lowest frequency for binning (default 0)")

    parser.add_argument("-u", "--upper_frequency",
                        default = 0,
                        help="Highest frequency for binning (default is all available)")

    args = parser.parse_args()
    start = int(args.start)
    number_samples = int(args.number_samples)
    number_bins = int(args.number_bins)
    upper_frequency = int(args.upper_frequency)

    # Regex for pulling a label string from a label touch file
    label_re = re.compile(r".*__label__(.*)$")
    
    # Feature set array and corresponding label array
    feature_set_array = []
    label_array = []

    # Iterate through sample subfolders in the dataset directory
    sample_folder_list = glob.glob(os.path.join(args.dataset, 'Samples') + '_[0-9]*')

    for sample_folder in sample_folder_list:
        label = 'Unlabeled'
        label_touch_files = glob.glob(os.path.join(sample_folder, '__label__') + '*')
        if len(label_touch_files) >= 1:
            label_match = label_re.match(label_touch_files[0])
            if label_match:
                label = label_match.group(1)

        # Collect features for each sample
        sample_list = glob.glob(os.path.join(sample_folder, 'sample') + '_[0-9]*')
        for wav_path in sample_list:
            Fs, data = read(wav_path)
            frq, ampl = getFFT(data, Fs, upper_frequency)
            feature_set_array.append(GetHistogram(ampl, number_bins))
            label_array.append(label)

    print feature_set_array
    print
    print label_array

    
if __name__ == "__main__":
    main()
