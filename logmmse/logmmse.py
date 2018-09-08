from __future__ import division
import numpy as np
from scipy.io.wavfile import read, write
from core import logmmse
from utils import to_float, from_float

np.seterr('raise')

def run_logmmse(input_filename, output_filename, initial_noise=6, window_size=0, noise_threshold=0.15,
                l_trim=False):
    fs, input_file = read(input_filename, 'r')
    # Left trim to prevent an error from the algorithm
    if l_trim:
        input_file = np.trim_zeros(input_file, 'f')
    output = np.array([], dtype=input_file.dtype)
    input_file, dtype = to_float(input_file)
    num_frames = len(input_file)

    chunk_size = int(np.floor(60*fs))
    saved_params = None
    frames_read = 0
    while frames_read < num_frames:
        frames = num_frames - frames_read if frames_read + chunk_size > num_frames else chunk_size
        signal = input_file[frames_read:frames_read + frames]
        frames_read = frames_read + frames
        _output, saved_params = logmmse(signal, fs, initial_noise, window_size, noise_threshold, saved_params)
        output = np.concatenate((output, from_float(_output, dtype)))
    write(output_filename, fs, output)

run_logmmse('./test/pcm1608m.wav', 'sample2.wav')
