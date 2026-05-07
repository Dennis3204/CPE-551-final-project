"""
data_loader.py

This file loads and cleans the NREL Alternative Fuel Stations CSV for New York.

The script turns the data in "data/alt_fuel_stations_ny.csv" into a cleaned Pandas DataFrame
"""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "Fuel Type Code",
    "Station Name",
    "City",
    "State",
    "ZIP",
    "Status Code",
    "Access Code",
    "EV Level1 EVSE Num",
    "EV Level2 EVSE Num",
    "EV DC Fast Count",
    "EV Network",
    "Latitude",
    "Longitude",
    "ID",
]

PORT_COLUMNS = [
    "EV Level1 EVSE Num",
    "EV Level2 EVSE Num",
    "EV DC Fast Count",
]

COLUMN_RENAMES = {
    "ID": "station_id",
    "Fuel Type Code": "fuel_type_code",
    "Station Name": "station_name",
    "City": "city",
    "State": "state",
    "ZIP": "zip_code",
    "Status Code": "status_code",
    "Access Code": "access_code",
    "EV Level1 EVSE Num": "level1",
    "EV Level2 EVSE Num": "level2",
    "EV DC Fast Count": "dc_fast",
    "EV Network": "network",
    "Latitude": "latitude",
    "Longitude": "longitude",
}


def load_stations(csv_path):
    """
    Read the NREL Alternative Fuel Stations CSV from disk.

    The function reads the file and checks that the columns the project needs exist, cleaning then happens 
    in a different function
    """
    path = Path(csv_path)

    try:
        df = pd.read_csv(path)
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Could not find NREL CSV at '{path.resolve()}'. "
            f"Make sure the file exists and the path is correct."
        ) from err
    except pd.errors.ParserError as err:
        raise ValueError(
            f"Failed to parse CSV at '{path.resolve()}': {err}"
        ) from err

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            "Input CSV is missing required column(s): "
            f"{missing}. Expected all of {REQUIRED_COLUMNS}."
        )

    return df


def clean_stations(df):
    """
    Clean the raw NREL DataFrame and turn it into a format that can be used
    """
    df = df.copy()

    # Keep only electric stations that are currently operational.
    df = df[df["Fuel Type Code"] == "ELEC"]
    df = df[df["Status Code"] == "E"]

    # drop rows without a location or ZIP
    df = df.dropna(subset=["Latitude", "Longitude", "ZIP"])

    # for port columns fill blanks with 0, coerce to int, and reject negatives.
    for col in PORT_COLUMNS:
        df[col] = df[col].fillna(0).astype(int)
        if (df[col] < 0).any():
            bad_count = int((df[col] < 0).sum())
            raise ValueError(
                f"Column '{col}' contains {bad_count} negative value(s); "
                f"port counts must be non-negative."
            )

    # clean up the zipcode format
    df["ZIP"] = (
        df["ZIP"]
        .astype(str)
        .str.strip()
        .str.split("-", n=1)
        .str[0]
        .str.zfill(5)
    )

    # keep only the columns we care about
    df = df[list(COLUMN_RENAMES.keys())].rename(columns=COLUMN_RENAMES)

    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)

    return df.reset_index(drop=True)


if __name__ == "__main__":
    default_path = Path(__file__).resolve().parent.parent / "data" / "alt_fuel_stations.csv"

    print(f"Smoke test: loading {default_path}")
    raw = load_stations(default_path)
    print(f"  Raw shape:    {raw.shape}")

    cleaned = clean_stations(raw)
    print(f"  Cleaned shape: {cleaned.shape}")
    print()
    print("First 5 rows of cleaned data:")
    print(cleaned.head())
