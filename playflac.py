#!/usr/bin/env python

# Simple test script that plays FLAC files

from __future__ import print_function

import sys
import soundfile
import getopt
import alsaaudio

def play(device, flac):
    rate = flac.samplerate
    channels = flac.channels

    print("{} channels, {} sampling rate".format(
        channels, rate
    ))

    # Set attributes
    device.setchannels(channels)
    device.setrate(rate)

    # write stuff to ALSA in 1/8 second chunks
    periodsize = int(rate / 8)
    device.setperiodsize(periodsize)

    # Soundfile will stuff as 32-bit with our read dtype below
    device.setformat(alsaaudio.PCM_FORMAT_S32_LE)

    for frame in flac.blocks(blocksize=periodsize, dtype="int32"):
        device.write(frame.tobytes())


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

    flac = soundfile.SoundFile(args[0])
    device = alsaaudio.PCM(device=device)

    play(device, flac)
