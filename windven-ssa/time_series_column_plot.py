import numpy as np

from data import read_file
from ssa import ssa_decompose

import matplotlib.pyplot as plt


def plot_time_series(data_source="wind.lst"):
    plt.style.use(style="seaborn-v0_8-talk")

    window_size = 40
    n_ssa_plots = 3

    data = read_file("data/" + data_source)

    # Resample and process data
    data = data.resample("M").mean().dropna()
    bt = data["bt"]

    # Singular Spectrum Analysis
    bt_ssa, periods = ssa_decompose(bt, window_size=window_size)

    # Plotting
    fig, axes = plt.subplots(n_ssa_plots+1, 1, figsize=(7, 6))

    # Plot original
    axes[0].plot(bt, "-", label="Monthly Bt")
    axes[0].set_xlim(left=data.index[0], right=data.index[-1])
    #axes[0].get_xaxis().set_visible(False)
    axes[0].set_ylabel("Bt (nT)", size="medium")
    axes[0].legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, handlelength=0, handletextpad=0)

    # Plot SSA results
    for i in range(n_ssa_plots):
        if i != n_ssa_plots-1:
            axes[i+1].plot(bt.index, bt_ssa[0, i],
                           label=f"SSA {i+1},\n{round(periods[i])} months")
        else:
            # Plot the remaining components:
            bt_ssa_2 = np.empty(np.shape(bt_ssa[0, 0]))
            for j in range(len(bt_ssa[0, ]) - n_ssa_plots):
                bt_ssa_2 += bt_ssa[0, i + j]
            axes[i + 1].plot(bt.index, bt_ssa_2,
                             label="Sum of\nremaining\ncomponents")

        if i == 0:
            axes[i+1].set_title(r"=", y=1.095)
        else:
            axes[i+1].set_title("+", y=1.095)
        axes[i+1].set_xlim(left=data.index[0], right=data.index[-1])
        axes[i+1].set_ylabel("Bt (nT)", size="medium")
        if i != n_ssa_plots-1:
            axes[i+1].get_xaxis().set_visible(False)
            axes[i+1].set_xlabel("Years", size="medium")
        axes[i + 1].legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, handlelength=0, handletextpad=0)

    plt.tight_layout()

    plt.show()
