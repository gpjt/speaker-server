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
    subtype = flac.subtype

    print("{} channels, {} sampling rate, {} subtype".format(
        channels, rate, subtype
    ))

    arhgt

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

    flac = soundfile.SoundFile(args[0])
    device = alsaaudio.PCM(device=device)

    play(device, flac)
