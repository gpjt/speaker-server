#!/usr/bin/env python

# Simple test script that plays (some) wav files

from __future__ import print_function

import sys
from mpg123 import Mpg123
import getopt
import alsaaudio

def play(device, mp3):    
    rate, channels, encoding = mp3.get_format()

    print("{} channels, {} sampling rate, {} encoding".format(
        channels, rate, encoding
    ))

    width = mp3.get_width_by_encoding(encoding)
    print("width comes out as {}".format(width))

    # Set attributes
    device.setchannels(channels)
    device.setrate(rate)

    # 8bit is unsigned in wav files
    if width == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif width == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif width == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_3LE)
    elif width == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    periodsize = int(rate / 8)

    device.setperiodsize(periodsize)
    
    for frame in mp3.iter_frames():
        device.write(frame)


def usage():
    print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    device = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        usage()
        
    mp3 = Mpg123(args[0])
    device = alsaaudio.PCM(device=device)

    play(device, mp3)
