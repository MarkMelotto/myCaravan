from logging import exception

import pandas as pd
import os
from pathlib import Path
import xarray as xr



def rename_camels_files_csv(postfix="zim") -> xr.Dataset:
    default_folder = Path.home()
    default_folder = default_folder / "PycharmProjects/myCaravan/outputs/"
    directory = default_folder / f"output_{postfix}" / "timeseries"
    if not directory.is_dir():
        raise ValueError(f"The provided folder for '{postfix}' is not a valid directory.")
    df = pd.DataFrame()
    # first the CSV bit
    csv_path = directory / "csv" / f"{postfix}"
    for root, dirs, files in os.walk(csv_path):
        for file in files:
            if file.endswith(".csv"):
                filepath = Path(root) / file
                gauge_id = f"{file[:11]}"
                # print(gauge_id)

                temp_df = pd.read_csv(filepath)
                # Optional: add filename or catchment ID as a column
                temp_df[f"gauge_id"] = gauge_id
                # Append to the main DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)
    return df.to_xarray()


def rename_camels_files_nc(postfix="zim") -> xr.Dataset:
    default_folder = Path.home()
    default_folder = default_folder / "PycharmProjects/myCaravan/outputs/"
    directory = default_folder / f"output_{postfix}" / "timeseries"
    netcdf_path = directory / "netcdf" / f"{postfix}"

    datasets = []

    for root, dirs, files in os.walk(netcdf_path):
        for file in files:
            if file.endswith(".nc"):
                filepath = Path(root) / file
                gauge_id = file[:11]

                try:
                    temp_ds = xr.open_dataset(filepath, engine='netcdf4')
                    # Add gauge_id as a coordinate or attribute
                    temp_ds = temp_ds.assign_coords(gauge_id=gauge_id)
                    datasets.append(temp_ds)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # Combine all datasets
    if datasets:
        combined_ds = xr.concat(datasets, dim="gauge_id")
        return combined_ds
    else:
        print("No NetCDF files found.")
        raise FileNotFoundError("No NetCDF files found.")


if __name__ == "__main__":
    ds_csv = rename_camels_files_csv("zim")

    ds = rename_camels_files_nc

    print(ds.head())
