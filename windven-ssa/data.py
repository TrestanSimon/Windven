from datetime import datetime
import numpy as np
import pandas as pd

_MONTH_DAYS = [
    31,  # Jan
    28,  # Feb
    31,  # Mar
    30,  # Apr
    31,  # May
    30,  # Jun
    31,  # Jul
    31,  # Aug
    30,  # Sep
    31,  # Oct
    30,  # Nov
    31,  # Dec
]


def read_file(file_name):
    time = []
    data = {"bt": [], "bx": [], "by": [], "bz": []}
    with open(file_name, 'r') as f:
        for line in f:
            columns = line.strip().split()
            year, day, hour = map(int, columns[0:3])
            time.append(_to_datetime(year, day, hour))

            bt, bx, by, bz = map(_process_data, columns[3:])
            data["bt"].append(bt)
            data["bx"].append(bx)
            data["by"].append(by)
            data["bz"].append(bz)

        return pd.DataFrame(data, index=time)


def _to_datetime(year, day, hour):
    month_days = _MONTH_DAYS
    if year % 4 == 0:
        month_days[1] = 29
    else:
        month_days[1] = 28

    month = 0
    while day > 0:
        day -= month_days[month]
        month += 1

    day += month_days[month-1]

    return datetime(year, month, day, hour)


def _process_data(value):
    value = float(value)
    if value == 999.9:
        value = np.NaN
    return value


def resample_no_nan(values):
    if any(pd.isna(values)):
        return np.nan
    else:
        return np.mean(values)
