#!/usr/bin/python

from __future__ import division
import numpy as np
import math
from scipy.special import *
from scikits.audiolab import Sndfile, Format
import argparse
import sys

def logmmse(x, Srate, noise_frames=6, Slen=0, eta=0.15):
    if Slen == 0:
        Slen = int(math.floor(0.02 * Srate))

    if Slen % 2 == 1:
        Slen = Slen + 1

    PERC = 50
    len1 = math.floor(Slen * PERC / 100)
    len2 = int(Slen - len1)

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

    aa = 0.98
    mu = 0.98
    eta = 0.15
    ksi_min = 10 ** (-25 / 10)

    for k in range(0, Nframes*len2, len2):
        insign = win * x[k:k + Slen]

        spec = np.fft.fft(insign, nFFT, axis=0)
        sig = np.absolute(spec)
        sig2 = sig ** 2

        gammak = np.minimum(sig2 / noise_mu2, 40)

        if k == 0:
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

    return xfinal

#main

parser = argparse.ArgumentParser(description='Speech enhancement/noise reduction using Log MMSE STSA algorithm')
parser.add_argument('input_file', action='store', type=str, help='input file to clean')
parser.add_argument('output_file', action='store', type=str, help='output file to write (default: stdout)', default=sys.stdout)
parser.add_argument('-i, --initial-noise', action='store', type=int, dest='initial_noise', help='initial noise in frames (default: 6)', default=6)
parser.add_argument('-w, --window-size', action='store', type=int, dest='window_size', help='hanning window size (default: 0.02*sample rate)', default=0)
parser.add_argument('-n, --noise-threshold', action='store', type=float, dest='noise_threshold', help='noise thresold (default: 0.15)', default=0.15)
args = parser.parse_args()

input_file = Sndfile(args.input_file, 'r')

fs = input_file.samplerate
num_frames = input_file.nframes

output_file = Sndfile(args.output_file, 'w', Format(type=input_file.file_format, encoding='pcm16', endianness=input_file.endianness), input_file.channels, fs)

chunk_size = int(np.floor(60*fs))

frames_read = 0
while (frames_read < num_frames):
    frames = num_frames - frames_read if frames_read + chunk_size > num_frames else chunk_size
    signal = input_file.read_frames(frames)
    frames_read = frames_read + frames

    output = logmmse(signal, fs, args.initial_noise, args.window_size, args.noise_threshold)

    output = np.array(output*np.iinfo(np.int16).max, dtype=np.int16)
    output_file.write_frames(output)

input_file.close()
output_file.close()
