#!/usr/bin/python

from __future__ import division
import numpy as np
import math
from scipy.special import *
from numpy.matlib import repmat
from scipy.signal import lfilter
from scipy.io import wavfile
from scikits.audiolab import Sndfile, Format
import argparse
import sys

def logmmse(x, Srate, noise_frames=6):
    Slen = int(math.floor(20 * Srate / 1000))

    if Slen % 2 == 1:
        Slen = Slen + 1

    PERC = 50
    len1 = math.floor(Slen * PERC / 100)
    len2 = Slen - len1

    win = np.hanning(Slen)
    win = win * len2 / np.sum(win)
    nFFT = 2 * Slen

    noise_mean = np.zeros(nFFT)
    for j in range(0, Slen*noise_frames, Slen):
        noise_mean = noise_mean + np.absolute(np.fft.fft(win * x[j:j + Slen], nFFT, axis=0))
    noise_mu2 = noise_mean / noise_frames ** 2

    x_old = np.zeros(len1)
    Nframes = int(math.floor(len(x) / len2) - math.floor(Slen / len2))
    xfinal = np.zeros(Nframes * len2)

    k = 0
    aa = 0.98
    mu = 0.98
    eta = 0.15
    ksi_min = 10 ** (-25 / 10)

    for n in range(Nframes):
        insign = win * x[k:k + Slen]

        spec = np.fft.fft(insign, nFFT, axis=0)
        sig2 = np.absolute(spec) ** 2

        gammak = np.minimum(sig2 / noise_mu2, 40)

        if n == 0:
            ksi = aa + (1 - aa) * np.maximum(gammak - 1, 0)
        else:
            ksi = aa * Xk_prev / noise_mu2 + (1 - aa) * np.maximum(gammak - 1, 0)
            ksi = np.maximum(ksi_min, ksi)

        log_sigma_k = gammak * ksi/(1 + ksi) - np.log(1 + ksi)
        vad_decision = np.sum(log_sigma_k)/Slen
        if (vad_decision < eta):
            noise_mu2 = mu * noise_mu2 + (1 - mu) * sig2

        A = ksi / (1 + ksi)
        vk = A * gammak
        ei_vk = 0.5 * expn(1, vk)
        hw = A * np.exp(ei_vk)

        sig = sig * hw
        Xk_prev = sig ** 2
        xi_w = np.fft.ifft(hw * spec, nFFT, axis=0)
        xi_w = np.real(xi_w)

        xfinal[k:k + len2] = x_old + xi_w[0:len1]
        x_old = xi_w[len1:Slen]
        k = k + len2

    return xfinal

#main

fs, signal = wavfile.read(sys.argv[1])
signal = np.array(signal/32767, dtype=np.float)

output = logmmse(signal, fs)

output = np.array(output*32767, dtype=np.int16)
wavfile.write(sys.argv[2], fs, output)
