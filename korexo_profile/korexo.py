from datetime import datetime

import numpy as np
import pandas as pd


def read(fn, encoding="utf-16", parse_dts=True, datefmt="%d/%m/%Y"):
    record = {}
    record["created_file"] = datetime.fromtimestamp(os.path.getctime(fn))
    record["modified_file"] = datetime.fromtimestamp(os.path.getmtime(fn))
    p_offset = 4
    with open(fn, "rb") as f:
        for i, line in enumerate(f.read().decode(encoding).splitlines()):
            if line.startswith("FILE CREATED"):
                created_stated = line.split(",", 1)[1].strip()
                record["created_info"] = created_stated
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
                record["header_line_no"] = i + 1
                params_ = line.split(",")
                params = params_[p_offset:]
                record["params"] = params
                record["sensors"] = sensors
                record["means"] = means
                record["stdevs"] = stdevs
    df = pd.read_csv(fn, skiprows=(record["header_line_no"] - 1), encoding=encoding, )
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
                    try:
                        data = [ts.date() for ts in pd.to_datetime(data, format=datefmt, errors="coerce")]
                    except:
                        print("Error coercing data")
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
    record["datasets"] = datasets
    return record