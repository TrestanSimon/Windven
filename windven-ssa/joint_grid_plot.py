from data import read_file

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['text.usetex'] = True
plt.style.use(style="seaborn-v0_8-talk")

data = read_file("data/wind.lst")
print(data)

data_day = data.resample("H").mean()

g = sns.JointGrid(
    data_day,
    x="by",
    y="bz",
    space=0,
)

size = 10

g.ax_joint.set(xlabel=r"$B_y$ (nT)", ylabel="$B_z$ (nT)")

g.ax_joint.set_xlim(left=-size, right=size)
g.ax_joint.set_ylim(bottom=-size, top=size)

g.plot_joint(
    sns.kdeplot,
    fill=True,
    clip=((-size, size), (-size, size)),
    thresh=0,
    levels=200,
    cmap='Blues',
)
g.plot_marginals(sns.histplot, color="#03051A", alpha=0.5, bins=100)

plt.show()
