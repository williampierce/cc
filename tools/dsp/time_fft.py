#!/usr/bin/env python

import argparse
import numpy as np
from dspUtils import get_fft

DEFAULT_SIZE = 320000
DEFAULT_COUNT = 10

def main():
    parser = argparse.ArgumentParser(
        description =
        'Compute FFTs of test data. Useful for timing.')
    parser.add_argument("-s", "--size", type=int,
                        default=DEFAULT_SIZE,
                        help="Number of data points (default {})".format(DEFAULT_SIZE))
    parser.add_argument("-c", "--count", type=int,
                        default=DEFAULT_COUNT,
                        help="Number of repetitions (default {})".format(DEFAULT_COUNT))

    args = parser.parse_args()
    size= int(args.size)
    count= int(args.count)
    Fs = 32000
    data = np.ones(size)

    for idx in range(count):
        frq, ampl = get_fft(data, Fs, 0)

    print "FFT complete, size={}, count={}, len(frq)={}".format(size, count, len(frq))

if __name__ == "__main__":
    main()

