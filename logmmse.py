#!/usr/bin/python

from __future__ import division
import numpy as np
from scipy.io.wavfile import read, write
from core import logmmse
from utils import type_conversion

np.seterr('raise')


def run_logmmse(input_filename, output_filename, initial_noise=6, window_size=0, noise_threshold=0.15):
    fs, input_file = read(input_filename, 'r')
    output = np.array([], dtype=input_file.dtype)
    input_file = type_conversion(input_file)
    num_frames = len(input_file)

    chunk_size = int(np.floor(60*fs))
    saved_params = None
    frames_read = 0
    while frames_read < num_frames:
        frames = num_frames - frames_read if frames_read + chunk_size > num_frames else chunk_size
        signal = input_file[frames_read:frames_read + frames]
        frames_read = frames_read + frames
        _output, saved_params = logmmse(signal, fs, initial_noise, window_size, noise_threshold, saved_params)

        _output = np.array(_output*np.iinfo(np.int16).max, dtype=np.int16)
        output = np.concatenate((output, _output))
    write(output_filename, fs, output)
