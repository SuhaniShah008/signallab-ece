import numpy as np
from signallab import *

FS = 8000


def _gain_db(filt, f0):
    f, m = freq_response(filt, FS, n=4096)
    return m[np.argmin(np.abs(f - f0))]


def test_fir_lowpass_passes_and_stops():
    h = design_fir(800, FS, numtaps=121)
    assert _gain_db(h, 200) > -1
    assert _gain_db(h, 3000) < -40


def test_butter_lowpass_passes_and_stops():
    sos = design_butter(800, FS, order=6)
    assert _gain_db(sos, 200) > -1
    assert _gain_db(sos, 3000) < -60


def test_filtering_improves_snr():
    _, clean = multitone([200], [1.0], FS, 1.0)
    _, interferer = multitone([3000], [0.8], FS, 1.0)
    noisy = add_noise(clean + interferer, 5)
    out = apply_filter(noisy, design_butter(800, FS), zero_phase=True)
    assert snr_db(clean, out) > snr_db(clean, noisy) + 5


def test_spectrum_peak_location():
    _, x = multitone([1000], [1.0], FS, 1.0)
    f, m = magnitude_spectrum(x, FS)
    assert abs(f[np.argmax(m)] - 1000) < 2


def test_add_noise_hits_target_snr():
    _, x = multitone([500], [1.0], FS, 2.0)
    assert abs(snr_db(x, add_noise(x, 10)) - 10) < 0.5
