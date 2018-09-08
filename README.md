The fork improved on the original version to support Python 3, fix a few bugs, and make it importable from other Python scripts

## logmmse ##
A python implementation of the LogMMSE speech enhancement/noise reduction alogrithm. This file has been ported from logmmse.m file found at the following link.

## API Reference ##

### run_logmmse(input_filename, output_filename, initial_noise=6, window_size=0, noise_threshold=0.15, l_trim=False) ###

**input_filename (Mandatory)**

filename of the wave input

supported format: 32-bit floating-point, 32-bit PCM, 16-bit PCM, and 8-bit PCM, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html     

**output_filename (Mandatory)**

filename of the wave output

the format would be the same as input     

**l_trim**

Whether to remove zeros at the beginning of an array, set this option to true if you encounter the following error:
```
sig = sig * hw
FloatingPointError: invalid value encountered in multiply
```

### Reference ###

https://raw.githubusercontent.com/braindead/Noise-reduction/master/logmmse.m
