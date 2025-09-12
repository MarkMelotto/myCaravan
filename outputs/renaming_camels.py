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
    csv_path = directory / "csv" / "postfix"
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
    netcdf_path = directory / "netcdf" / "postfix"
    for root, dirs, files in os.walk(netcdf_path):
        for file in files:
            if file.endswith(".nc"):
                filepath = Path(root) / file
                new_filename = f"{file[:11]}{file[-3:]}"
                new_filepath = Path(root) / new_filename
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filepath} to {new_filepath}")


test_name = "zim_1457800.0.nc"

file = Path.home()
file = file / "PycharmProjects/myCaravan/outputs/output_zim/timeseries/netcdf/zim/zim_1457800.0.nc"
df = xr.read_csv(file)
print(df)

