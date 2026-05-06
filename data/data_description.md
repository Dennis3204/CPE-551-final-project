# Data Dictionary — `alt_fuel_stations_ny.csv`

**Source:** NREL Alternative Fuel Stations (<https://afdc.energy.gov/stations>)
**Scope:** New York State
**Downloaded:** May 6, 2026

The raw CSV has ~70 columns covering all alternative fuels. The project uses only the columns below.

## Columns used

| Column | Type | Description |
|---|---|---|
| `Fuel Type Code` | str | Fuel category. Keep only `ELEC`. |
| `Station Name` | str | Station name. |
| `City` | str | City. |
| `State` | str | Two-letter state code (`NY`). |
| `ZIP` | str | 5-digit ZIP. |
| `Status Code` | str | Operational status. Keep only `E` (available). |
| `Access Code` | str | `public` or `private`. |
| `EV Level1 EVSE Num` | int | Level 1 ports. |
| `EV Level2 EVSE Num` | int | Level 2 ports. |
| `EV DC Fast Count` | int | DC Fast ports. |
| `EV Network` | str | Charging network operator. |
| `Latitude` | float | Decimal-degree latitude. |
| `Longitude` | float | Decimal-degree longitude. |

## Filtering

1. `Fuel Type Code == 'ELEC'`
2. `Status Code == 'E'`
3. Drop rows missing `Latitude`, `Longitude`, or `ZIP`.
4. Port counts: fill missing with `0`, must be non-negative.
5. Strip `-####` Plus 4 suffix from ZIP.
