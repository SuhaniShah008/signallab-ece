import numpy as np


def multitone(freqs, amps, fs, duration):
    """Sum of sinusoids. Returns (t, x)."""
    t = np.arange(0, duration, 1 / fs)
    x = sum(a * np.sin(2 * np.pi * f * t) for f, a in zip(freqs, amps))
    return t, x


def add_noise(x, snr_target_db, seed=0):
    """Add white Gaussian noise so the result has the requested SNR (dB)."""
    rng = np.random.default_rng(seed)
    p_signal = np.mean(x ** 2)
    p_noise = p_signal / (10 ** (snr_target_db / 10))
    return x + rng.normal(0, np.sqrt(p_noise), size=x.shape)
