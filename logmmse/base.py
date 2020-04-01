from __future__ import division
import numpy as np
from scipy.io.wavfile import read, write
from .logmmse import logmmse as _logmmse
from .utils import to_float, from_float

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
        _output, saved_params = _logmmse(signal, fs, initial_noise, window_size, noise_threshold, saved_params)
        m_output = np.concatenate((m_output, from_float(_output, dtype)))
    return m_output

def logmmse(data, sampling_rate, output_file=None, initial_noise=6,
            window_size=0, noise_threshold=0.15):
    data, dtype = to_float(data)
    data += np.finfo(np.float64).eps
    if data.ndim == 1:
        output = mono_logmmse(data, sampling_rate, dtype, initial_noise, window_size,
                              noise_threshold)
    else:
        output = []
        for _, m_input in enumerate(data.T):
            output.append(mono_logmmse(m_input, sampling_rate, dtype, initial_noise,
                                       window_size, noise_threshold))
    output = np.array(output)
    if output_file is not None:
        write(output_file, sampling_rate, output.T)
    return output.T

def logmmse_from_file(input_file, output_file=None, initial_noise=6,
                      window_size=0, noise_threshold=0.15):
    sampling_rate, data = read(input_file, 'r')
    return logmmse(data, sampling_rate, output_file, initial_noise,
                   window_size, noise_threshold)
