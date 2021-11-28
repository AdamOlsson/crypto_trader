from os import listdir
import os
import pandas as pd

class DataSeries():
    col_names = ["Open time","Open","High","Low","Close","Volume","Close time",
                "Quote asset volume","Number of trades","Taker buy base asset volume",
                "Taker buy quote asset volume","Ignore"]

    relevant_cols = [col_names[0], col_names[1], col_names[2], col_names[3],col_names[4], col_names[6]]
    
    def __init__(self, data_path):
        csv_files = sorted(listdir(data_path)) # Sort by date, earliest first

        # read first csv
        path = os.path.join(data_path, csv_files[0])
        data_series = pd.read_csv(path, names=self.col_names)

        for _, csv_file in enumerate(csv_files, start=1):
            path = os.path.join(data_path, csv_file)
            df = pd.read_csv(path, names=self.col_names)
            data_series = data_series.append(df, ignore_index=True)

        self.data_series = data_series

    
    def __len__(self):
        return self.data_series.shape[0]

    def __getitem__(self, i):
        if isinstance(i, slice):
            raise Exception("Slicing not yet implemented.")
        else:
            return self.data_series[self.relevant_cols].iloc[i]


class DataSeries15m(DataSeries):
    data_path = "data/BTCEUR_15min_2020-03_to_2021-09"
    def __init__(self):
        super().__init__(self.data_path)

class DataSeries1m(DataSeries):
    data_path = "data/BTCEUR_1min_2021-09-12_to_2021-10-14"
    def __init__(self):
        super().__init__(self.data_path)

class DataSeries1mETHEUR(DataSeries):
    data_path = "data/ETHEUR_1min_2021-10-01_to_2021-10-29"
    def __init__(self):
        super().__init__(self.data_path)
    
