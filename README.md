The fork improved on the original version to support Python 3, fix a few bugs, and make it importable from other Python scripts

## logmmse ##
A python implementation of the LogMMSE speech enhancement/noise reduction alogrithm

## API Reference ##

### logmmse(data, sampling_rate, output_file=None, initial_noise=6, window_size=0, noise_threshold=0.15) ###

**data (Mandatory)**

A 1d or 2d (number of frames, channels) Numpy array representing the audio signal

Supported format: 32-bit floating-point, 32-bit PCM, 16-bit PCM, and 8-bit PCM, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html     

**sampling_rate (Mandatory)**

Sampling rate of the data (e.g. 16k/44.1 kHz)

**output_filename**

filename of the wave output. If none, no file would be generated

the output format would be the same as input

**return**

A 1d or 2d (number of frames, channels) Numpy array representing the enhanced signal

### logmmse_from_file(data, output_filename, initial_noise=6, window_size=0, noise_threshold=0.15) ###

**input_filename (Mandatory)**

Filename of the wave input

supported format: 32-bit floating-point, 32-bit PCM, 16-bit PCM, and 8-bit PCM, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html     

**output_filename**

See above

**return**

A 1d or 2d (number of frames, channels) Numpy array representing the enhanced signal

### Contribute ###

After opening an issue or pull request, please also send me an email for notification

### Reference ###

This file has been ported from logmmse.m file found at the following link.
https://raw.githubusercontent.com/braindead/Noise-reduction/master/logmmse.m
