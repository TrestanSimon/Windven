import matplotlib.pyplot as plt
import numpy as np

from memspectrum import MESA

from data import read_file
from ssa import ssa_decompose


def plot_forecast(datasource="wind.lst", n_ssa=2):
    plt.style.use(style="seaborn-v0_8-talk")

    window_size = 40

    data = read_file("data/" + datasource)
    data = data.resample("M").mean().dropna()

    bt = data["bt"]
    time = data.index

    forecast_length = back = 100
    n_sims = 100000

    bt_ssa, periods = ssa_decompose(bt, window_size=window_size)


    m = MESA()
    m.solve(bt_ssa[0, n_ssa][:-back])
    forecast = m.forecast(bt_ssa[0, n_ssa][:-back], length=forecast_length, number_of_simulations=n_sims, include_data=False)
    # Ensemble median
    median = np.median(forecast, axis=0)
    p5, p95 = np.percentile(forecast, (5, 95), axis=0)  # 90% credibility boundaries

    # Plotting
    fig, axes = plt.subplots(1, 1, figsize=(6, 6))

    axes.plot(time[:-back], bt_ssa[0, n_ssa][:-back], color="k")
    axes.fill_between(time[-back:], p5, p95, color="b", alpha=.5, label="90% Cr.")
    axes.plot(time[-back:], bt_ssa[0, n_ssa][-back:], color="k", linestyle="--", label="Observed data")
    axes.plot(time[-back:], median, color="r", label="Median estimate")

    axes.set_xlim(left=data.index[0], right=data.index[-1])
    axes.set_ylabel("Bt (nT)", size="medium")
    axes.legend(loc="best")

    plt.tight_layout()

    plt.show()
