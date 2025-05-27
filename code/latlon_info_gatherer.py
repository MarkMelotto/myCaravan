import pandas as pd
import os

def extract_latlon_etc(folder):
    directory = os.path.join("c:\\", "/Users/markmelotto/PycharmProjects/myCaravan")
    directory = os.path.join(directory, folder)
    # country = 'Ghana'
    country = folder.split('_')[-1]
    country = country[0].upper() + country[1:]
    df_metadata = pd.DataFrame(columns=[
        "gauge_lat",
        "gauge_lon",
        "gauge_name",
        "country",
        "area"
    ])

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                lat = lon = station = area = grdc_no = None


                with open(filepath, 'r') as f:
                    for line in f:
                        # print(line)
                        line = line.strip()
                        # print(line)

                        if line.startswith("# Latitude"):
                            lat = float(line.split(":")[1].strip())
                        elif line.startswith("# Longitude"):
                            lon = float(line.split(":")[1].strip())
                        elif line.startswith("# Station"):
                            station = line.split(":")[1].strip()
                        elif line.startswith("# GRDC-No."):
                            grdc_no_raw = line.split(":")[1].strip()
                            grdc_no = f"AF_{grdc_no_raw}.0"
                        elif line.startswith("# Catchment area ("):
                            area = float(line.split(":")[1].strip())
                            # print(area)

                        if line.startswith("# DATA") or line.startswith("YYYY-MM-DD"):
                            break

                # Only add to DataFrame if key fields are present
                if grdc_no and lat is not None and lon is not None and station:
                    df_metadata.loc[grdc_no] = {
                        "gauge_lat": lat,
                        "gauge_lon": lon,
                        "gauge_name": station,
                        "country": country,
                        "area": area
                    }
    df_metadata.to_csv(directory + "/df_metadata.csv", index=True)
    return df_metadata

if __name__ == "__main__":
    df_metadata = extract_latlon_etc("zoe")
    # Optional: show or save the DataFrame
    print(df_metadata)
    # df_metadata.to_csv(directory + "/df_metadata.csv", index=True)
    #
    #
    # df_2 = pd.read_csv(directory + "/df_metadata.csv", index_col=0)
    # print(df_2)