import numpy as np

def type_conversion(_input):
    if _input.dtype == np.float64:
        return _input
    elif _input.dtype == np.float32:
        return _input.astype(np.float64)
    elif _input.dtype == np.uint8:
        return (_input - 128) / 128.
    elif _input.dtype == np.int16:
        return _input / 32768.
    elif _input.dtype == np.int32:
        return _input / 2147483648
    raise ValueError('Unsupported wave file format, please contact the author')
