import numpy as np


def magnitude_spectrum(x, fs, window="hann"):
    """One-sided windowed FFT magnitude in dB (relative to full scale 1.0)."""
    n = len(x)
    w = np.hanning(n) if window == "hann" else np.ones(n)
    X = np.fft.rfft(x * w)
    mag = 2 * np.abs(X) / np.sum(w)
    return np.fft.rfftfreq(n, 1 / fs), 20 * np.log10(np.maximum(mag, 1e-12))


def snr_db(clean, test):
    """SNR of `test` relative to the `clean` reference, in dB."""
    noise = test - clean
    return 10 * np.log10(np.sum(clean ** 2) / np.sum(noise ** 2))
