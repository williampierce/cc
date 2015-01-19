#!/usr/bin/env python

import argparse
import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from mpl_toolkits.mplot3d import Axes3D

from dspUtils import get_fft, get_histogram

DEFAULT_NUMBER_SAMPLES = 5
DEFAULT_NUMBER_BINS = 8

def get_label_color_map(labels):
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    label_color_map = {}
    next_color = 0
    for label in labels:
        if label not in label_color_map:
            label_color_map[label] = colors[next_color]
            next_color = (next_color + 1) % len(colors)

    return label_color_map

def plot_features_3d(features, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = np.arange(len(features[0]))
    label_color_map = get_label_color_map(labels)

    for index in range(len(features)):
        ys = np.array(features[index])
        label_color = label_color_map[labels[index]]
        ax.bar(xs, ys, zs=index, zdir='y', color=label_color, alpha=0.7)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    

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
            frq, ampl = get_fft(data, Fs, upper_frequency)
            feature_set_array.append(get_histogram(ampl, number_bins))
            label_array.append(label)

    print feature_set_array
    print
    print label_array
    plot_features_3d(feature_set_array, label_array)

 
if __name__ == "__main__":
    main()
