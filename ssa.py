import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq
from pyts.decomposition import SingularSpectrumAnalysis
from memspectrum import MESA


def ssa_decompose(data, **kwargs):
    data = data.values.reshape(1, -1)
    ssa = SingularSpectrumAnalysis(**kwargs)
    data_ssa = ssa.fit_transform(data)

    periods = np.empty((len(data_ssa[0, ])))
    for i in range(len(data_ssa[0, ])):
        if i == 0:
            periods[i] = _fft_period(data_ssa[0, i])
        else:
            periods[i] = _mem_period(data_ssa[0, i])

    return data_ssa, abs(periods)


def _mem_period(data):
    frequencies, spectrum = _mem_spectrum(data)
    return 1.0 / frequencies[np.argmax(spectrum)]


def _fft_period(data):
    frequencies, spectrum = _fft_spectrum(data)
    peaks, _ = find_peaks(spectrum)
    peaks_height = spectrum[peaks]
    """frequencies, spectrum = _mem_spectrum(data)
    peaks, _ = find_peaks(spectrum)
    print(frequencies[peaks])"""
    return 1.0 / frequencies[peaks[np.argmax(peaks_height)]]


def _mem_spectrum(data):
    m = MESA()
    m.solve(data)
    return m.spectrum(1.0)


def _fft_spectrum(data):
    spectrum = abs(rfft(data))
    frequencies = rfftfreq(len(data))
    return frequencies, spectrum


def _plot_spectrum(data):
    fig, ax = plt.subplots(2)
    freq, spec = _mem_spectrum(data)
    ax[0].plot(freq, spec, 'o-')
    ax[1].plot(data)
    plt.show()
