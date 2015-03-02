#!/usr/bin/env python

import argparse
import os
import glob
import re
import itertools
import numpy as np

from scipy.io.wavfile import read

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


def get_label_features_map(dataset, upper_frequency, number_bins):
    """Create a dictionary mapping labels to arrays of feature sets
    :param dataset: absolute path to a folder of sample folders
    :rtype: dict, str -> array
    """
    # Iterate through sample subfolders in the dataset directory
    sample_folder_list = glob.glob(os.path.join(dataset, 'Samples') + '_[0-9]*')
    label_features_map = {}
    for sample_folder in sample_folder_list:
        label = get_sample_set_label(sample_folder)

        # Collect features for each sample
        sample_list = glob.glob(os.path.join(sample_folder, 'sample') + '_[0-9]*')
        feature_set_list = []
        for wav_path in sample_list:
            Fs, data = read(wav_path)
            frq, ampl = get_fft(data, Fs, upper_frequency)
            feature_set_list.append(get_histogram(ampl, number_bins))

        if label in label_features_map:
            label_features_map[label].extend(feature_set_list)
        else:
            label_features_map[label] = feature_set_list

    return label_features_map


def partition_dataset(label_features_map, train_fraction):
    """Break a dataset into feature and label arrays for training and test
    :param label_features_map: dictionary mapping labels to feature set arrays
    :return: features_train, labels_train, features_test, labels_test
    """
    # Create sklearn-compatible features and labels
    features = []
    labels = []
    features_train = []
    labels_train = []
    features_test = []
    labels_test = []
    for label, feature_set_list in label_features_map.items():
        sample_count = len(feature_set_list)
        features += feature_set_list
        labels += [label] * sample_count

        train_count = int(sample_count * train_fraction)
        features_train += feature_set_list[:train_count]
        labels_train += [label] * train_count

        features_test += feature_set_list[train_count:]
        labels_test += [label] * (sample_count - train_count)

    print "Samples: {0}, train: {1}/{2}, test: {3}/{4}".format(
        len(features), len(features_train), len(labels_train), len(features_test), len(labels_test))
    return features_train, labels_train, features_test, labels_test


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

    label_features_map = get_label_features_map(args.dataset, upper_frequency, number_bins)

    features_train, labels_train, features_test, labels_test = partition_dataset(label_features_map, train_fraction=0.8)

    #print features_train
    #print
    #print features_test

    #plot_features_3d(features, labels)
    #plot_features_3d(features_train, labels_train)
    #plot_features_3d(features_test, labels_test)


    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    run_classifier(clf, features_train, labels_train, features_test, labels_test)

    from sklearn import svm
    clf = svm.SVC(kernel='linear')
    run_classifier(clf, features_train, labels_train, features_test, labels_test)

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=10)
    run_classifier(knn, features_train, labels_train, features_test, labels_test)

    from sklearn.neighbors.nearest_centroid import NearestCentroid
    nc = NearestCentroid()
    run_classifier(nc, features_train, labels_train, features_test, labels_test)


if __name__ == "__main__":
    main()

