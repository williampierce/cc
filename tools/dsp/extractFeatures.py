#!/usr/bin/env python

import argparse
import os
import glob
import re
import itertools
import numpy as np
import scipy as sp
from sklearn import preprocessing

from scipy.io.wavfile import read

from dspUtils import get_fft

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


def run_classifier(clf, features_train, labels_train, features_test, labels_test):
    X = np.array(features_train)
    y = np.array(labels_train)

    clf.fit(X, y)

    test_count = 0
    success_count = 0
    for feature_set, label in itertools.izip(features_test, labels_test):
        test_count += 1
        predicted = clf.predict(feature_set)

        if label in predicted:
            success_count += 1

        print "Actual: {}, Predicted: {}".format(label, predicted)

    print "Success rate: {}".format(float(success_count)/test_count)


# Regex for pulling a label string from a label touch file
label_re = re.compile(r".*__label__(.*)$")

def get_sample_set_label(sample_folder):
    """Returns the label string embedded in the name of the __label__* touch file
    :param sample_folder: absolute path
    :rtype: str
    """
    label = 'Unlabeled'
    label_touch_files = glob.glob(os.path.join(sample_folder, '__label__') + '*')
    if len(label_touch_files) >= 1:
        label_match = label_re.match(label_touch_files[0])
        if label_match:
            label = label_match.group(1)
    return label


def get_label_samples_map(dataset, upper_frequency, number_bins):
    """Create a dictionary mapping labels to normalized (mean=0, std=1) numpy arrays of feature sets
    :param dataset: absolute path to a folder of sample folders
    :rtype: dict, str -> array
    """

    # We'll compute the mean and std using a one-pass online algorithm.
    # (See http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance.)
    sample_count = 0
    sample_mean = np.zeros(number_bins)
    sample_sum_squares = np.zeros(number_bins)

    # Iterate through sample subfolders in the dataset directory
    sample_folder_list = glob.glob(os.path.join(dataset, 'Samples') + '_[0-9]*')
    label_samples_map = {}
    for sample_folder in sample_folder_list:
        label = get_sample_set_label(sample_folder)

        # Create samples by extracting features from each wave file
        sample_list = glob.glob(os.path.join(sample_folder, 'sample') + '_[0-9]*')
        samples = np.empty([0, number_bins])
        for wav_path in sample_list:
            Fs, data = read(wav_path)
            frq, ampl = get_fft(data, Fs, upper_frequency)
            new_sample, bin_edges = np.histogram(ampl, number_bins, density=True)
            samples = np.append(samples, [new_sample], 0)

            # Update mean and variance
            sample_count += 1
            delta = new_sample - sample_mean
            sample_mean += delta/sample_count
            sample_sum_squares += delta*(new_sample - sample_mean)

        if label in label_samples_map:
            # Handle multiple sample folders with the same label
            label_samples_map[label] = np.append(label_samples_map[label], samples)
        else:
            label_samples_map[label] = samples

    # Use collected statistics to normalize data set
    sample_std = np.sqrt(sample_sum_squares/(sample_count-1)) if sample_count >= 2 else 1.0

    np.set_printoptions(precision=3)
    print "Mean: {}, Std: {}".format(sample_mean, sample_std)

    np_label_samples_map = {}
    for label, samples in label_samples_map.items():
        # Normalize samples
        #np_label_samples_map[label] = preprocessing.scale(np.array(samples))
        np_label_samples_map[label] = (samples - sample_mean)/sample_std

    return np_label_samples_map


def partition_dataset(num_features, label_samples_map, train_fraction):
    """Break a dataset into feature and label arrays for training and test
    :param label_samples_map: dictionary mapping labels to feature set arrays
    :return: samples_train, labels_train, samples_test, labels_test
    """
    # Create sklearn-compatible samples and labels
    labels = []
    labels_train = []
    labels_test = []
    samples_all = np.empty([0, num_features])
    samples_train = np.empty([0, num_features])
    samples_test = np.empty([0, num_features])
    for label, samples in label_samples_map.items():
        sample_count = len(samples)
        train_count = int(sample_count * train_fraction)

        labels += [label] * sample_count
        labels_train += [label] * train_count
        labels_test += [label] * (sample_count - train_count)

        samples_all = np.append(samples_all, samples, 0)
        samples_train = np.append(samples_train, samples[:train_count], 0)
        samples_test = np.append(samples_test, samples[train_count:], 0)

    print "Samples: {0}, train: {1}/{2}, test: {3}/{4}".format(
        len(samples_all), len(samples_train), len(labels_train), len(samples_test), len(labels_test))
    return samples_train, labels_train, samples_test, labels_test


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

    label_samples_map = get_label_samples_map(args.dataset, upper_frequency, number_bins)

    samples_train, labels_train, samples_test, labels_test =\
        partition_dataset(number_bins, label_samples_map, train_fraction=0.8)

    #print samples_train
    print
    print "Train mean: {}, std: {}".format(np.mean(samples_train, 0), np.std(samples_train, 0))
    print
    #print samples_test
    print "Test mean: {}, std: {}".format(np.mean(samples_test, 0), np.std(samples_test, 0))
    print

    #plot_samples_3d(samples, labels)
    #plot_samples_3d(samples_train, labels_train)
    #plot_samples_3d(samples_test, labels_test)


    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    run_classifier(clf, samples_train, labels_train, samples_test, labels_test)

    from sklearn import svm
    clf = svm.SVC(kernel='linear')
    run_classifier(clf, samples_train, labels_train, samples_test, labels_test)

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=10)
    run_classifier(knn, samples_train, labels_train, samples_test, labels_test)

    from sklearn.neighbors.nearest_centroid import NearestCentroid
    nc = NearestCentroid()
    run_classifier(nc, samples_train, labels_train, samples_test, labels_test)


if __name__ == "__main__":
    main()

