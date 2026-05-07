# EV Charging Access Gap Analyzer (New York State)

A Python tool that uses the NREL Alternative Fuel Stations dataset to identify regions of New York with the largest gaps in public EV charging access.

## Team Members

- **Dennis Ren** — dren4@stevens.edu — 20014453
- **Dritan Xhelilaj** — dxhelila@stevens.edu

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
CPE-551-final-project/
├── data/
│   ├── alt_fuel_stations.csv
│   └── data_description.md
├── src/
│   ├── charging_station.py
│   ├── region_profile.py
│   ├── data_loader.py
│   ├── analysis.py
│   └── visualize.py
├── tests/
│   └── test.py
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
