#!/usr/bin/env python

import numpy as np
from dspUtils import get_fft


def main():
    Fs = 32000
    data = np.ones(320000)
    frq, ampl = get_fft(data, Fs, 0)

    print "FFT complete. Fs={}, size={}".format(Fs, len(frq))

if __name__ == "__main__":
    main()

