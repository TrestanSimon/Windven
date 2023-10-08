from data import read_file, resample_no_nan
from ssa import ssa_decompose

import matplotlib.pyplot as plt


plt.rcParams['text.usetex'] = True
plt.style.use(style="seaborn-v0_8-talk")

data = read_file("data\\wind.lst")

# Resample and process data
data = data.resample("M").mean().dropna()
bt = data["bt"]
window_size = 40

# Singular Spectrum Analysis
bt_ssa, periods = ssa_decompose(bt, window_size=window_size)

# Plotting
plt.figure(figsize=(6, 6))

ax1 = plt.subplot(211)
ax1.plot(bt, '-', label=r'Monthly averaged $B_t$')
ax1.legend(loc='best')
ax1.get_xaxis().set_ticklabels([])
ax1.set_xlim(left=data.index[0], right=data.index[-1])
ax1.set_ylabel(r"$B_t$ (nT)")
# ax1.annotate("23", xy=(0.225, 0.2), xycoords="axes fraction", fontsize=14)
# ax1.annotate("24", xy=(0.7, 0.2), xycoords="axes fraction", fontsize=14)
# ax1.annotate("25", xy=(0.95, 0.2), xycoords="axes fraction", fontsize=14)

ax2 = plt.subplot(212)
for i in range(3):
    ax2.plot(bt.index, bt_ssa[0, i], label=f"SSA {round(periods[i])}")
ax2.legend(loc='best')
ax2.set_xlim(left=data.index[0], right=data.index[-1])
ax2.set_ylabel(r"$B_t$ (nT)")

plt.suptitle(r'SSA of Monthly Averaged $B_t$')

plt.tight_layout()

plt.show()
