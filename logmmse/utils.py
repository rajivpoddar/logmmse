from __future__ import division
import numpy as np

def to_float(_input):
    if _input.dtype == np.float64:
        return _input, _input.dtype
    elif _input.dtype == np.float32:
        return _input.astype(np.float64), _input.dtype
    elif _input.dtype == np.uint8:
        return (_input - 128) / 128., _input.dtype
    elif _input.dtype == np.int16:
        return _input / 32768., _input.dtype
    elif _input.dtype == np.int32:
        return _input / 2147483648., _input.dtype
    raise ValueError('Unsupported wave file format, please contact the author')

def from_float(_input, dtype):
    if dtype == np.float64:
        return _input, np.float64
    elif dtype == np.float32:
        return _input.astype(np.float32)
    elif dtype == np.uint8:
        return ((_input * 128) + 128).astype(np.uint8)
    elif dtype == np.int16:
        return (_input * 32768).astype(np.int16)
    elif dtype == np.int32:
        print(_input)
        return (_input * 2147483648).astype(np.int32)
    raise ValueError('Unsupported wave file format, please contact the author')
