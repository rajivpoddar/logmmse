from __future__ import division
import numpy as np
from scipy.io.wavfile import read, write
from logmmse import logmmse
from utils import to_float, from_float

np.seterr('raise')

def mono_logmmse(m_input, fs, dtype, initial_noise=6, window_size=0, noise_threshold=0.15):
    num_frames = len(m_input)
    chunk_size = int(np.floor(60*fs))
    m_output = np.array([], dtype=dtype)
    saved_params = None
    frames_read = 0
    while frames_read < num_frames:
        frames = num_frames - frames_read if frames_read + chunk_size > num_frames else chunk_size
        signal = m_input[frames_read:frames_read + frames]
        frames_read = frames_read + frames
        _output, saved_params = logmmse(signal, fs, initial_noise, window_size, noise_threshold, saved_params)
        m_output = np.concatenate((m_output, from_float(_output, dtype)))
    return m_output

def run_logmmse(input_filename, output_filename, initial_noise=6, window_size=0, noise_threshold=0.15):
    fs, input_file = read(input_filename, 'r')
    output = np.array([], dtype=input_file.dtype)
    input_file, dtype = to_float(input_file)
    if input_file.ndim == 1:
        output = mono_logmmse(input_file, fs, dtype, initial_noise, window_size, noise_threshold)
    else:
        for _, m_input in enumerate(input_file.T):
            output = np.concatenate((output, mono_logmmse(m_input, fs, dtype, initial_noise, window_size, noise_threshold)))
    write(output_filename, fs, output.T)
