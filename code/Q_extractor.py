import pandas as pd
import os
import numpy as np

def extract_Q(folder):
    directory = os.path.join("c:\\", "/Users/markmelotto/PycharmProjects/myCaravan")
    directory = os.path.join(directory, folder)
    df_2 = pd.read_csv(directory + "/df_metadata.csv")
    # print(df_2)
    counter = 0
    # print(df_2["Unnamed: 0"][counter])
    df_loaded = pd.DataFrame()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("Day.csv"):
                filepath = os.path.join(root, file)


                with open(filepath, 'r') as f:
                    camel = df_2["Unnamed: 0"][counter]
                    data = pd.read_csv(f,
                                       delimiter=";",
                                       names=["local time", "time", camel],
                                       parse_dates=["local time"],
                                       skiprows=37  # Skipping the header row if necessary
                                       # skiprows = 1  # Skipping the header row if necessary
                    )
                    # print(data)
                    data["local time"] = pd.to_datetime(data["local time"], errors="coerce")

                    data.set_index("local time", inplace=True)

                    # Remove unnecessary 'time' column since it's always "--:--"
                    data.drop(columns=["time"], inplace=True)
                    # data = pd.to_datetime(data)
                    data[camel] = pd.to_numeric(data[camel], errors="coerce")
                    data.replace(-999.000, np.nan, inplace=True)
                    area = df_2["area"][counter]
                    # data[camel] = data[camel] * area / (1000 * 86400)  # convert mm/d to m^3/s
                    data[camel] = data[camel] * 86400 / (area * 1e3)  # convert m^3/s to mm/d

                    # Merge by date (outer join on 'local time')
                    if df_loaded.empty and counter == 0:
                        df_loaded = data
                    else:
                        df_loaded = pd.merge(df_loaded, data, on="local time", how="outer")

                    print(f"Loaded data for {camel}")
                    # print(df_loaded)
                    counter += 1
                    # break
    return df_loaded

if __name__ == "__main__":
    '''NOTE; first csv file should contain data, I think I fixed that problem though'''
    # print(df_loaded)
    df_loaded = extract_Q("zoe")
    # df_loaded.to_csv(directory + "/df_loaded.csv", index=True)
    #
    # df_2 = pd.read_csv(directory + "/df_loaded.csv", index_col=0)
    print(df_loaded.head())