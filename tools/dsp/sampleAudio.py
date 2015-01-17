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

def touch_file(file_path):
    open(file_path, 'a').close()

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
                        help="Duration of each sample (default {} seconds)".format(DEFAULT_DURATION_SECS))

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
    sample_folder_list = glob.glob(os.path.join(args.root_dir, 'Samples') + '_[0-9]*')
    print "Found {} sample folders".format(len(sample_folder_list))
    new_folder_number = 0
    for folder_name in sample_folder_list:
        folder_number = int(folder_name.split('_')[1])
        if folder_number >= new_folder_number:
            new_folder_number = folder_number + 1

    print "New folder number: {}".format(new_folder_number)

    # Create comment string if the comment contains non-blank characters
    # Create sample folder name
    if(args.comment and args.comment.strip(" ")):
        comment_string = args.comment.strip(" ").replace(" ", "_")
        summary_string = "d{0}_n{1}__{2}".format(args.duration, args.number_samples, comment_string)
        # sample_folder_name = "Samples_{0}_{1}".format(str(new_folder_number).zfill(3), get_timestamp())
        sample_folder_name = "Samples_{0}_{1}".format(str(new_folder_number).zfill(3), summary_string)
    else:
        summary_string = "d{0}_n{1}".format(args.duration, args.number_samples)
        sample_folder_name = "Samples_{0}".format(str(new_folder_number).zfill(3))

    # Create folder for samples
    sample_folder_name = "Samples_{0}__{1}".format(str(new_folder_number).zfill(3), summary_string)
    sample_dir_path = os.path.join(args.root_dir, sample_folder_name)
    print "Creating sample directory: " + sample_dir_path
    mkdir_p(sample_dir_path)

    # Place comment file in sample folder
    if(args.comment):
        summary_filename = "__{}__".format(summary_string)
        summary_path = os.path.join(sample_dir_path, summary_filename)
        touch_file(summary_path)

    start_timestamp = get_timestamp()

    for i in range(args.number_samples):
        # Create sample path for audio file
        sample_filename = "sample_{0}.wav".format(str(i).zfill(3))

        sample_path = os.path.join(sample_dir_path, sample_filename)
        print "[{0}/{1}] ********** {2} **********".format(i+1, args.number_samples, sample_filename)

        sample_audio(sample_path, args.duration)

    end_timestamp = get_timestamp()
    timestamp_touch_filename = "__{0}__to__{1}__".format(start_timestamp, end_timestamp)
    #timestamp_touch_file_path = os.path.join(sample_dir_path, timestamp_touch_filename)
    touch_file(os.path.join(sample_dir_path, timestamp_touch_filename))


if __name__ == "__main__":
    main()

