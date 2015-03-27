#!/usr/bin/env python

import argparse
import numpy as np
import scipy as sp
from extractFeatures import get_label_samples_map, partition_dataset

DEFAULT_NUMBER_SAMPLES = 5
DEFAULT_NUMBER_BINS = 8


def build_gaussian_model(samples, labels, print_distance):
    """Build up a gaussian model of the data; show the successive mean and variance with each new instance"""
    for i in range(len(samples)):
        # For now, don't worry about efficiency
        count = i+1

        # mean and std_dev are vectors
        mean = np.sum(samples[:count], 0)/float(count)
        std_dev = np.sqrt(np.sum(np.power(samples[:count] - mean, 2), 0)/float(count))

        np.set_printoptions(precision=3)

        if not print_distance:
            print '[{:3d}] {}: mean: {}, std_dev: {}'.format(count, labels[count-1], mean, std_dev)

        # Calculate the distance (in current std_devs) of the next point from the current mean
        elif 1 < count < len(samples):
            dist = np.sqrt(np.sum(np.power((samples[count] - mean)/std_dev, 2)))
            print '[{:3d}] {}: std_dev: {}, dist: {}'.format(count, labels[count], std_dev, dist)


def get_label_stats_map(label_samples_map):
    """Compute the mean and std dev for the samples corresponding to each label"""

    for label, samples in label_samples_map.items():
        count = np.size(samples, 0)

        # mean and std_dev are vectors
        mean = np.mean(samples, 0)
        std = np.std(samples, 0)
        print '{}: mean: {}, std_dev: {}'.format(label, mean, std)


def main():
    parser = argparse.ArgumentParser(
        description =
        'Create a feature set array and a corresponding label array from a dataset of \'Sample_NNN\' subfolders.')
    parser.add_argument("dataset",
                        help="path to dataset folder containing samples folders")

    parser.add_argument("-b", "--number_bins", type=int,
                        default=DEFAULT_NUMBER_BINS,
                        help="Number of bins (default {})".format(DEFAULT_NUMBER_BINS))

    parser.add_argument("-l", "--lower_frequency",
                        default = 0,
                        help="Lowest frequency for binning (default 0)")

    parser.add_argument("-u", "--upper_frequency",
                        default = 0,
                        help="Highest frequency for binning (default is all available)")

    args = parser.parse_args()
    number_bins = int(args.number_bins)
    upper_frequency = int(args.upper_frequency)

    # Collect raw feature data
    label_samples_map = get_label_samples_map(args.dataset, upper_frequency, number_bins)

    get_label_stats_map(label_samples_map)
    '''
    samples_train, labels_train, samples_test, labels_test =\
        partition_dataset(number_bins, label_samples_map, train_fraction=0.8)

    build_gaussian_model(samples_train, labels_train, False)
    build_gaussian_model(samples_train, labels_train, True)
    '''

if __name__ == "__main__":
    main()
