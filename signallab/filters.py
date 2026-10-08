import numpy as np
from scipy import signal


def design_fir(cutoff_hz, fs, numtaps=101, kind="lowpass", window="hamming"):
    """Windowed-sinc FIR design. cutoff_hz may be a float or [low, high]."""
    return signal.firwin(numtaps, cutoff_hz, fs=fs, pass_zero=kind, window=window)


def design_butter(cutoff_hz, fs, order=4, kind="lowpass"):
    """Butterworth IIR design as second-order sections (numerically stable)."""
    return signal.butter(order, cutoff_hz, btype=kind, fs=fs, output="sos")


def apply_filter(x, filt, zero_phase=False):
    """Apply an FIR (1-D taps) or IIR (SOS matrix) filter."""
    filt = np.asarray(filt)
    if filt.ndim == 1:  # FIR
        return signal.filtfilt(filt, [1.0], x) if zero_phase else signal.lfilter(filt, [1.0], x)
    return signal.sosfiltfilt(filt, x) if zero_phase else signal.sosfilt(filt, x)


def freq_response(filt, fs, n=2048):
    """Return (freqs_hz, magnitude_dB) for an FIR or SOS filter."""
    filt = np.asarray(filt)
    if filt.ndim == 1:
        w, h = signal.freqz(filt, worN=n, fs=fs)
    else:
        w, h = signal.sosfreqz(filt, worN=n, fs=fs)
    return w, 20 * np.log10(np.maximum(np.abs(h), 1e-12))
