#!/usr/bin/env python

import argparse
import os
import subprocess
import glob
from datetime import datetime

DEFAULT_ROOT_DIR       = os.getcwd()
DEFAULT_DURATION_SECS  = 10
DEFAULT_NUMBER_SAMPLES = 20

def mkdir_p(path):
    """
    mkdir, but don't complain if it already exists (like "mkdir -p")
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_timestamp():
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

def sample_audio(sample_path, duration):
    # rec -r 44100 -b 16 test.wav trim 0 5 // record, 44100 hz, 16 bit, 5 seconds
    cmd_args = ['rec', '-r', '32000', '-b', '16', sample_path, 'trim', '0', str(duration)]
    subprocess.call(args=cmd_args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root_dir",
                        default=DEFAULT_ROOT_DIR, 
                        help="Root directory for sample collections (default {})".format(DEFAULT_ROOT_DIR)) 

    parser.add_argument("-d", "--duration", type=int,
                        default=DEFAULT_DURATION_SECS,
                        help="Duration of each sample (default {})".format(DEFAULT_DURATION_SECS))

    parser.add_argument("-n", "--number_samples", type=int,
                        default=DEFAULT_NUMBER_SAMPLES,
                        help="Number of samples (default {})".format(DEFAULT_NUMBER_SAMPLES))

    parser.add_argument("-c", "--comment",
                        help="Provide comments or tags for this sample set")

    args = parser.parse_args()

    print "Starting sample collection, root_dir: {0}, duration: {1}, number_samples: {2}".format(
        args.root_dir, args.duration, args.number_samples)

    # Check for sample directories already present
    # Sample folders have the form Samples_<number>_timestamp
    sample_folder_list = glob.glob(os.path.join(args.root_dir, 'Samples') + '_[0-9]*_*')
    print "Found {} sample folders".format(len(sample_folder_list))
    new_folder_number = 0
    for folder_name in sample_folder_list:
        folder_number = int(folder_name.split('_')[1])
        if folder_number >= new_folder_number:
            new_folder_number = folder_number + 1

    print "New folder number: {}".format(new_folder_number)

    # Create folder for samples
    sample_folder_name = "Samples_{0}_{1}".format(str(new_folder_number).zfill(3), get_timestamp())
    sample_dir_path = os.path.join(args.root_dir, sample_folder_name)
    print "Creating sample directory: " + sample_dir_path
    mkdir_p(sample_dir_path)

    # Place comment file in directory
    if(args.comment):
        comment_filename = "_{}_".format(args.comment).replace(" ", "_")
        # comment_path = os.path.join(sample_dir_path, comment_filename.replace(" ", "_"))
        comment_path = os.path.join(sample_dir_path, comment_filename)
        open(comment_path, 'a').close()

    for i in range(args.number_samples):
        # Create sample path for audio file
        sample_filename = "sample_{0}_{1}.wav".format(str(i).zfill(3), get_timestamp())

        sample_path = os.path.join(sample_dir_path, sample_filename)
        print "[{0}] ********** Collecting sample: {1} **********".format(i, sample_filename)

        sample_audio(sample_path, args.duration)

if __name__ == "__main__":
    main()

