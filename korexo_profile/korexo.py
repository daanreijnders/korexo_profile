from collections import defaultdict
from datetime import datetime
from pathlib import Path
import os

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from scipy.interpolate import interp1d


def convert_numeric(v):
    if v == "NA":
        return pd.NA
    else:
        return pd.to_numeric(v)


def read(fn, encoding="utf-16", parse_dts=True, datefmt="auto"):
    record = {}
    md = {}
    md["created_file"] = datetime.fromtimestamp(os.path.getctime(fn))
    md["modified_file"] = datetime.fromtimestamp(os.path.getmtime(fn))
    p_offset = 4
    with open(fn, "rb") as f:
        for i, line in enumerate(f.read().decode(encoding).splitlines()):
            if line.startswith("FILE CREATED"):
                created_stated = line.split(",", 1)[1].strip()
                md["created_info"] = created_stated
            elif "MEAN VALUE:" in line:
                means_line = line.split(",")
                means = [convert_numeric(x) for x in means_line[p_offset:]]
            elif "STANDARD DEVIATION:" in line:
                stdev_line = line.split(",")
                stdevs = [convert_numeric(x) for x in stdev_line[p_offset:]]
            elif "SENSOR SERIAL NUMBER:" in line:
                sensor_line = line.split(",")
                sensors = sensor_line[p_offset:]
            elif line.startswith("Date ("):
                md["header_line_no"] = i + 1
                params_ = line.split(",")
                params = params_[p_offset:]
                md["params"] = params
                md["sensors"] = sensors
                md["means"] = means
                md["stdevs"] = stdevs
    df = pd.read_csv(fn, skiprows=(md["header_line_no"] - 1), encoding=encoding, )
    datasets = []
    for i in range(len(params_)):
        param = params_[i]
        if i >= p_offset:
            pi = i - p_offset
            data = df[param].values
            if len(np.unique(data)) == 1:
                median = data[0]
            else:
                try:
                    median = np.median(data)
                except TypeError:
                    median = data[0]
            dataset = {
                "name": params[pi],
                "column": param,
                "sensor": sensors[pi],
                "mean": means[pi],
                "stdev": stdevs[pi],
                "data": data,
                "median": median,
            }
            datasets.append(dataset)
        else:
            param = params_[i]
            if "(" in param:
                name = param.split("(", 1)[0].strip()
            else:
                name = param
            data = df[param].values
            if parse_dts:
                if name == "Date":
                    if datefmt == "auto":
                        unitfmt = param.split("(", 1)[1][:-1].strip()
                        if unitfmt == "MM/DD/YYYY":
                            datefmt = "%m/%d/%Y"
                        elif unitfmt == "DD/MM/YYYY":
                            datefmt = "%d/%m/%Y"
                    try:
                        data = [ts.date() for ts in pd.to_datetime(data, format=datefmt, errors="coerce")]
                    except:
                        pass
            if len(np.unique(data)) == 1:
                median = data[0]
            else:
                try:
                    median = np.median(data)
                except TypeError:
                    median = data[0]
            dataset = {
                "name": name,
                "column": param,
                "sensor": "",
                "mean": pd.NA,
                "stdev": pd.NA,
                "data": data,
                "median": median,
            }
            datasets.append(dataset)
    record["metadata"] = md
    record["datasets"] = datasets
    record["dataframe"] = df
    return record


COL_MAPPING = defaultdict(lambda: "NA")
COL_MAPPING.update({
    "Date (MM/DD/YYYY)": "date",
    "Time (HH:mm:ss)": "time",
    "Time (Fract. Sec)": "time_sec",
    "Site Name": "site",
    "Cond µS/cm": "cond",
    "Depth m": "water_depth",
    "nLF Cond µS/cm": "cond_nlf",
    "ODO % sat": "do_sat",
    "ODO % local": "do_local",
    "ODO mg/L": "do_conc",
    "ORP mV": "orp_mv",
    "Pressure psi a": "press",
    "Sal psu": "sal_psu",
    "SpCond µS/cm": "spcond",
    "TDS mg/L": "tds",
    "pH": "ph",
    "pH mV": "ph_mv",
    "Temp °C": "temp",
    "Vertical Position m": "vert_pos",
    "Battery V": "battery",
    "Cable Pwr V": "cable_power",
})

def convert_datasets_to_df(datasets, mapping=COL_MAPPING):
    """Convert a list of datasets to a dataframe, include renaming of
    column names if desired.

    Args:
        datasets (list): see output of :func:`korexo_profile.read`.
        mapping (dict): optional

    Returns: pandas dataframe with "datetime" column added.

    """
    df = pd.DataFrame({mapping[dset['column']]: dset['data'] for dset in datasets})
    timestamp = df["date"].astype(str) + " " + df["time"].astype(str)
    timestamps = pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")
    df.insert(0, "datetime", timestamps)
    return df


def make_regularly_spaced(df, index_col="dtw", step=0.05, step_precision=5):
    index_min = np.round(df[index_col].min(), 0) - 1
    while index_min < df[index_col].min():
        index_min += step
    index_min = np.round(index_min - step, step_precision)
    
    index_max = np.round(df[index_col].max(), 0) + 1
    while index_max > df[index_col].max():
        index_max -= step
    index_max = np.round(index_max + step, step_precision)

    index_new = np.linspace(index_min, index_max, int((index_max - index_min) / step) + 1)

    new_df = {}
    groupby = df.groupby(index_col)
    for col in df.columns:
        if is_numeric_dtype(df[col]) and not col == index_col:
            series = groupby[col].mean()
            data = interp1d(series.index, series.values, assume_sorted=True, bounds_error=False)(index_new)
            new_df[col] = data
    return pd.DataFrame(new_df, index=index_new).rename_axis(index_col)