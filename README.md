# EV Charging Access Gap Analyzer (New York State)

A Python tool that uses the NREL Alternative Fuel Stations dataset to identify regions of New York with the largest gaps in public EV charging access.

## Team Members

- **Dennis Ren** — dren4@stevens.edu — 20014453
- **Dritan [Last Name]** — 

## Description

The analyzer loads NREL station data, models each charger as a `ChargingStation` and aggregates them into `RegionProfile` objects (by county or ZIP). It then computes a weighted **gap score** combining station density, fast-charger ratio, and public-access ratio to rank the most underserved regions, and visualizes the results with Matplotlib.

## Dependencies

- `pandas`
- `matplotlib`
- `numpy`
- `pytest`
- `jupyter`

## Project Structure

```
final_project/
├── data/
│   └── alt_fuel_stations_ny.csv
├── src/
│   ├── charging_station.py
│   ├── region_profile.py
│   ├── data_loader.py
│   ├── analysis.py
│   └── visualize.py
├── tests/
│   ├── test_charging_station.py
│   ├── test_region_profile.py
│   └── test_analysis.py
├── main.ipynb
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook main.ipynb
```

Run the test suite:

```bash
pytest tests/
```
