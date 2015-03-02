#!/usr/bin/env python

import argparse
import os
import subprocess
import glob
from datetime import datetime
import re

DEFAULT_ROOT_DIR = os.getcwd()


def touch_file(file_path):
    open(file_path, 'a').close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root_dir",
                        default=DEFAULT_ROOT_DIR, 
                        help="Root directory for sample collections (default {})".format(DEFAULT_ROOT_DIR)) 

    args = parser.parse_args()

    # Check for sample directories already present
    # Sample folders have the form Samples_<number>_timestamp
    parameter_touch_file_list = glob.glob(os.path.join(args.root_dir, 'Samples') + '_[0-9]*/__d*')
    print "Found {} parameter touch files".format(len(parameter_touch_file_list))

    for parameter_touch_file in parameter_touch_file_list:
        label_touch_file = parameter_touch_file\
            .replace('/__d10_n20__', '/__label__')\
            .replace('_cadence_30__', '')\
            .replace('_cadence_60__', '')\
            .replace('_cadence_80__', '')
        print label_touch_file
        touch_file(label_touch_file)

    return


if __name__ == "__main__":
    main()

