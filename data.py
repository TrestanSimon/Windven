from datetime import datetime
import numpy as np

MONTH_DAYS = [
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
    data = {
        "time": [],
        "wind": [],
        "ace": [],
    }
    with open(file_name, 'r') as f:
        for line in f:
            columns = line.strip().split()
            year, month, hour = map(int, columns[0:3])
            data["time"].append(to_datetime(year, month, hour))
            
            value = map(float, columns[3:])

            if value == 999.9:
                value = np.NaN
        return data


def to_datetime(year, day, hour):
    month_days = MONTH_DAYS
    if year % 4 == 0:
        month_days[1] += 1

    month = 0
    while day > 0:
        day -= month_days[month]
        month += 1

    day += month_days[month-1]

    return datetime(year, month, day, hour)


for time, data in read_file("data\\imp_wind_ace_geo_mag_5TPpAZVoI_.lst"):
    print(f"{time}, {data}")
