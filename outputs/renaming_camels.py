import pandas as pd
import os
from pathlib import Path
import xarray as xr

default_folder = Path.home()
default_folder = default_folder / "PycharmProjects/myCaravan/outputs/"


def rename_camels_files(postfix="zim"):
    directory = default_folder / f"output_{postfix}" / "timeseries"
    if not directory.is_dir():
        raise ValueError(f"The provided folder for '{postfix}' is not a valid directory.")

    # first the CSV bit
    csv_path = directory / "csv" / f"{postfix}"
    for root, dirs, files in os.walk(csv_path):
        for file in files:
            if file.endswith(".csv"):
                filepath = Path(root) / file
                new_filename = f"{file[:11]}{file[-4:]}"
                new_filepath = Path(root) / new_filename
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filepath} to {new_filepath}")
    # Done with the CSV bit

    # now the netCDF bit
    netcdf_path = directory / "netcdf" / f"{postfix}"
    for root, dirs, files in os.walk(netcdf_path):
        for file in files:
            if file.endswith(".nc"):
                filepath = Path(root) / file
                new_filename = f"{file[:11]}{file[-3:]}"
                new_filepath = Path(root) / new_filename
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filepath} to {new_filepath}")


def rename_attributes_files(postfix="zim"):
    directory = default_folder / f"output_{postfix}" / "attributes"
    if not directory.is_dir():
        raise ValueError(f"The provided folder for '{postfix}' is not a valid directory.")

    caravan_attributes = directory / f"{postfix}" / f"attributes_caravan_{postfix}.csv"
    hydroatlas_attributes = directory / f"{postfix}" / f"attributes_hydroatlas_{postfix}.csv"
    other_attributes = directory / f"{postfix}" / f"attributes_other_{postfix}.csv"

    list_attributes = [caravan_attributes, hydroatlas_attributes, other_attributes]

    for csv in list_attributes:
        df = pd.read_csv(csv)
        for i, gauge in enumerate(df["gauge_id"]):
            # print(gauge[:4] + gauge[4:])
            new_gauge = gauge[:4] + str(int(float(gauge[4:])))
            # print(new_gauge)
            df.loc[i, "gauge_id"] = new_gauge

        df.to_csv(csv, index=False)

if __name__ == "__main__":


    # rename_camels_files()

    rename_attributes_files()