import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

from time_series_column_plot import plot_time_series
from forecast_plot import plot_forecast

root = tk.Tk()
root.geometry("300x300")
root.title("Windven-SSA demo")

data_source = tk.StringVar()
ssa_comp = tk.StringVar()


def generate_time_series():
    plot_time_series(
        str(data_source.get())
    )


def generate_forecast():
    plot_forecast(
        str(data_source.get()),
        int(ssa_comp.get())
    )


data_source_label = ttk.Label(root, text="Data source:")
data_source_label.pack(fill="x", padx=5, pady=5)
r1 = ttk.Radiobutton(root, text='ACE (278 months)', value='ace.lst', variable=data_source)
r1.pack(fill="x", padx=5, pady=2)
r2 = ttk.Radiobutton(root, text='Wind (341 months)', value='wind.lst', variable=data_source)
r2.pack(fill="x", padx=5, pady=2)

ssa_comp_label = ttk.Label(root, text="SSA component to forecast (>0):")
ssa_comp_label.pack(fill="x", padx=5, pady=5)
ssa_comp_entry = ttk.Entry(root, textvariable=ssa_comp)
ssa_comp_entry.pack(fill="x", padx=5, pady=5)

time_series_button = tk.Button(root, text="Plot SSA components", command=generate_time_series)
time_series_button.pack(fill="x", padx=5, pady=5)

forecast_button = tk.Button(root, text="Compare forecast with original data", command=generate_forecast)
forecast_button.pack(fill="x", padx=5, pady=5)

root.mainloop()
