# EV Charging Access Gap Analyzer (New York State)

A Python tool that uses the U.S. Department of Energy / NREL **Alternative Fuel
Stations** dataset to identify the regions of New York State with the largest
gaps in public electric‑vehicle (EV) charging access, and to visualize where
the state's charging buildout is uneven.

## Team Members


| Name            | Email                                               | Stevens ID |
| --------------- | --------------------------------------------------- | ---------- |
| Dennis Ren      | [dren4@stevens.edu](mailto:dren4@stevens.edu)       | 20014453   |
| Dritan Xhelilaj | [dxhelila@stevens.edu](mailto:dxhelila@stevens.edu) | 20014066   |


## Project Description

### Problem

New York State is pushing hard for people to switch to electric vehicles, but
the public charging network has not grown evenly. Some cities have plenty of
fast chargers, while other parts of the state have very few, or none at all.
Before anyone can decide where to build new chargers, it helps to first see
which areas are the most underserved today.

### Solution Approach

This project takes the NREL Alternative Fuel Stations dataset for New York and
turns it into a simple ranking of which regions have the worst charging access.

The program reads the CSV with `pandas`, cleans it up, and then groups the
stations by region. Each station becomes a `ChargingStation` object, and each
region becomes a `RegionProfile` that holds all of its stations together.

For every region, the program calculates a "gap score" between 0 and 1, where
0 means the region has great charging access and 1 means it has almost none.
The score combines three things: how few stations the region has, how many
of those stations support DC Fast charging, and how many are open to the
public. The regions are then sorted from worst to best, and `matplotlib`
draws three charts so the results are easy to look at: a bar chart of the
most underserved regions, a stacked chart showing the mix of charger types,
and a scatter plot of every station on a rough map of New York.

Everything is put together in `main.ipynb`, which runs the full pipeline
from loading the data to showing the final charts.

### Dependencies / Libraries

- `pandas` — CSV I/O, cleaning, and grouping
- `numpy` — numeric support for `pandas`
- `matplotlib` — all visualizations
- `pytest` — test runner
- `jupyter` — notebook for`main.ipynb`
- Standard library: `math`, `pathlib`

Tested with **Python 3.12**

### File / Module Structure

```
CPE-551-final-project/
├── data/
│   ├── alt_fuel_stations.csv       # raw NREL dataset (NY state)
│   └── data_description.md         # column-level data dictionary
├── src/
│   ├── charging_station.py         # ChargingStation class
│   ├── region_profile.py           # RegionProfile class (composition + __add__/__len__)
│   ├── data_loader.py              # load + clean NREL CSV (pandas)
│   ├── analysis.py                 # gap_score, rank_regions, underserved_regions, set ops
│   └── visualize.py                # matplotlib charts
├── tests/
│   └── test.py                     # pytest cases
├── main.ipynb                      # main program
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run the Program

1. Clone the repository and enter the project root:
  ```bash
   git clone https://github.com/Dennis3204/CPE-551-final-project.git
   cd CPE-551-final-project
  ```
2. Install the dependencies:
  ```bash
   pip install -r requirements.txt
  ```
3. Launch the main program (Jupyter Notebook):
  ```bash
   jupyter notebook main.ipynb
  ```
4. Run the test suite:
  ```bash
   pytest tests/
  ```

## Main Contributions of Each Team Member

Both members contributed equally.

### Dennis Ren

- Repository setup and `README.md`.
- `ChargingStation` class (`src/charging_station.py`).
- Data loading and cleaning (`src/data_loader.py`).
- Underserved‑region generator and set/recursion helpers in `src/analysis.py`.
- `main.ipynb` notebook.

### Dritan Xhelilaj

- NREL dataset and `data/data_description.md`.
- `RegionProfile` class (`src/region_profile.py`).
- Core of `src/analysis.py` (`build_regions`, `gap_score`, `rank_regions`).
- Matplotlib charts in `src/visualize.py`.
- Pytest cases in `tests/test.py`.

