from datetime import datetime
from pathlib import Path
import os

import numpy as np
import pandas as pd


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