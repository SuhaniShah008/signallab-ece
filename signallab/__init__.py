"""SignalLab: a small DSP toolkit for filter design and spectrum analysis."""
from .signals import multitone, add_noise
from .filters import design_fir, design_butter, apply_filter, freq_response
from .spectrum import magnitude_spectrum, snr_db

__all__ = ["multitone", "add_noise", "design_fir", "design_butter",
           "apply_filter", "freq_response", "magnitude_spectrum", "snr_db"]
