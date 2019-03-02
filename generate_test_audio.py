import os

import numpy as np
import soundfile


def create_waveform(frequency, length, samples_per_second):
    cycles_to_generate = frequency * length
    radians_to_generate = cycles_to_generate * 2 * np.pi
    samples_to_generate = length * samples_per_second
    radians = np.linspace(start=0, stop=radians_to_generate, num=int(samples_to_generate))
    wave = np.sin(radians) * 0.75
    return np.column_stack((wave, wave))


def generate_test_audio(samples_per_second):
    middle_c = 261.625565
    tune = np.row_stack((
        create_waveform(frequency=middle_c, length=2, samples_per_second=samples_per_second),
        create_waveform(frequency=2 * middle_c, length=1, samples_per_second=samples_per_second),
        create_waveform(frequency=1.5 * middle_c, length=3, samples_per_second=samples_per_second),
    ))
    return tune


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-audio")

    samples_per_second = 96000
    data = generate_test_audio(samples_per_second=samples_per_second)
    soundfile.write(os.path.join(output_dir, "tune-16x96000.wav"), data, samples_per_second, subtype="PCM_16")
    soundfile.write(os.path.join(output_dir, "tune-16x96000.flac"), data, samples_per_second, subtype="PCM_16")
    soundfile.write(os.path.join(output_dir, "tune-24x96000.wav"), data, samples_per_second, subtype="PCM_24")
    soundfile.write(os.path.join(output_dir, "tune-24x96000.flac"), data, samples_per_second, subtype="PCM_24")
