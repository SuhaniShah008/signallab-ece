"""Denoise a noisy 3-tone signal with FIR vs. IIR filters and save plots to docs/."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from signallab import *

FS = 8000
t, clean = multitone([200, 500, 3000], [1.0, 0.6, 0.8], FS, 1.0)  # 3 kHz = "interference"
noisy = add_noise(clean, snr_target_db=5)

fir = design_fir(800, FS, numtaps=121)
iir = design_butter(800, FS, order=6)
y_fir = apply_filter(noisy, fir, zero_phase=True)
y_iir = apply_filter(noisy, iir, zero_phase=True)

# Reference: what the signal should look like with only the wanted tones
_, wanted = multitone([200, 500], [1.0, 0.6], FS, 1.0)
print(f"SNR noisy : {snr_db(wanted, noisy):6.2f} dB")
print(f"SNR FIR   : {snr_db(wanted, y_fir):6.2f} dB")
print(f"SNR IIR   : {snr_db(wanted, y_iir):6.2f} dB")

fig, ax = plt.subplots(3, 1, figsize=(10, 9))
for sig, label in [(noisy, "Noisy input"), (y_fir, "FIR filtered"), (y_iir, "IIR filtered")]:
    f, m = magnitude_spectrum(sig, FS)
    ax[0].plot(f, m, label=label, lw=1)
ax[0].set(xlim=(0, FS / 2), ylim=(-100, 5), title="Spectrum", xlabel="Hz", ylabel="dB")
ax[0].legend(); ax[0].grid(alpha=.3)

for h, label in [(fir, "FIR (121 taps)"), (iir, "Butterworth (order 6)")]:
    f, m = freq_response(h, FS)
    ax[1].plot(f, m, label=label)
ax[1].set(ylim=(-100, 5), title="Filter frequency response", xlabel="Hz", ylabel="dB")
ax[1].legend(); ax[1].grid(alpha=.3)

n = slice(0, 400)
ax[2].plot(t[n], noisy[n], alpha=.4, label="Noisy")
ax[2].plot(t[n], y_iir[n], label="IIR filtered")
ax[2].plot(t[n], wanted[n], "k--", lw=1, label="Target")
ax[2].set(title="Time domain (first 50 ms)", xlabel="s"); ax[2].legend(); ax[2].grid(alpha=.3)

plt.tight_layout(); plt.savefig("docs/demo.png", dpi=130)
print("Saved docs/demo.png")
