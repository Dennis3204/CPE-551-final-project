"""
analysis.py

This turns a cleaned NREL DataFrame into RegionProfile objects and then scores each
region's "EV charging access gap", and then ranks the regions from worst to best.
"""

import math

from src.charging_station import ChargingStation
from src.region_profile import RegionProfile


# Component weights for the gap score. They sum to 1.0 so the final
# score is in between [0.0, 1.0]
# 0 means "very well served", 1 means
# "no charging access at all".
SCARCITY_WEIGHT = 0.5
FAST_WEIGHT = 0.25
PUBLIC_WEIGHT = 0.25


def build_regions(df, region_col="city"):
    """
    Group the cleaned NREL DataFrame into RegionProfile objects.
    """
    if region_col not in df.columns:
        raise KeyError(
            f"region_col '{region_col}' is not a column of the "
            f"DataFrame; available columns are {list(df.columns)}."
        )

    regions = {}

    for region_index, (region_value, group) in enumerate(
        df.groupby(region_col, sort=False)
    ):
        region_name = str(region_value)
        profile = RegionProfile(region_name=region_name, region_type=region_col)
        # Stamp the build-order index onto the profile so downstream
        # code (charts, debug prints) has a stable integer handle.
        profile.region_index = region_index

        for row in group.itertuples(index=False):
            station = ChargingStation(
                station_id=getattr(row, "station_id"),
                name=getattr(row, "station_name"),
                city=getattr(row, "city"),
                zip_code=getattr(row, "zip_code"),
                latitude=getattr(row, "latitude"),
                longitude=getattr(row, "longitude"),
                level1=getattr(row, "level1"),
                level2=getattr(row, "level2"),
                dc_fast=getattr(row, "dc_fast"),
                network=getattr(row, "network"),
                access_code=getattr(row, "access_code"),
                status_code=getattr(row, "status_code"),
            )
            profile.add_station(station)

        regions[region_name] = profile

    return regions


def gap_score(region, population=None):
    """
    this function computes a 0 to 1 "EV charging access gap" score for one region.

    The score is a weighted combination of three normalized factors:

        scarcity_factor = 1 / (1 + log1p(stations_or_per_capita))
        fast_factor     = 1 - fast_chargers   / total_stations
        public_factor   = 1 - public_stations / total_stations

        score = 0.5 * scarcity + 0.25 * fast_gap + 0.25 * public_gap
    """
    if population is not None and population <= 0:
        raise ValueError(
            f"population must be a positive integer, got {population!r}."
        )

    total = region.total_stations()
    # Empty region
    if total == 0:
        return 1.0

    if population is None:
        scarcity_basis = total
    else:
        # Stations per 10,000 residents
        # this is what charging benchmarks (e.g., NYSERDA reports) typically publish in.
        scarcity_basis = total / population * 10_000

    scarcity_factor = 1.0 / (1.0 + math.log1p(scarcity_basis))
    fast_factor = 1.0 - (region.fast_charger_count() / total)
    public_factor = 1.0 - (len(region.public_stations()) / total)

    score = (
        SCARCITY_WEIGHT * scarcity_factor
        + FAST_WEIGHT * fast_factor
        + PUBLIC_WEIGHT * public_factor
    )
    # each component is bounded in [0, 1] and the weights sum to 1,
    # so score is already in [0, 1] but this will make sure of that
    return max(0.0, min(1.0, score))


def rank_regions(regions):
    """
    Rank a regions dict from highest gap score (worst) to lowest.

    this function uses a lambda as the sort key
    """
    scored = [(name, gap_score(profile)) for name, profile in regions.items()]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored


def underserved_regions(regions, threshold):
    """
    yield (region_name, score) for every region that has a gap score
    that exceeds the threshold.
    """
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError(
            f"threshold must be in [0.0, 1.0], got {threshold!r}."
        )

    for region_name, profile in regions.items():
        score = gap_score(profile)
        if score > threshold:
            yield (region_name, score)


def network_overlap(region_a, region_b):
    """
    Return the set of charging networks operating in both regions.
    """
    return region_a.unique_networks() & region_b.unique_networks()


def networks_only_in(region_a, region_b):
    """
    Return networks that operate in "region_a" but not in "region_b".
    """
    return region_a.unique_networks() - region_b.unique_networks()


def recursive_total(regions_list):
    """
    Recursively sum "total_ports()" across a list of RegionProfiles.
    """
    if not regions_list:
        return 0
    return regions_list[0].total_ports() + recursive_total(regions_list[1:])


if __name__ == "__main__":
    #testing
    from pathlib import Path

    from src.data_loader import clean_stations, load_stations

    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "alt_fuel_stations.csv"
    )

    print(f"Smoke test: loading {csv_path}")
    df = clean_stations(load_stations(csv_path))
    regions = build_regions(df, region_col="city")
    print(f"  Built {len(regions)} city-level RegionProfiles.\n")

    # generater testing: stream the top underserved cities above a
    THRESHOLD = 0.75
    print(f"Underserved cities (gap_score > {THRESHOLD}):")
    for rank, (name, score) in enumerate(
        underserved_regions(regions, THRESHOLD), start=1
    ):
        print(f"  #{rank:>2} {name:<25} score={score:.3f}")
        if rank >= 10:
            break
    print()

    # pick the two regions with the most
    # stations and compare their network rosters.
    by_size = sorted(
        regions.values(), key=lambda r: r.total_stations(), reverse=True
    )
    if len(by_size) >= 2:
        a, b = by_size[0], by_size[1]
        print(f"Comparing networks: '{a.region_name}' vs '{b.region_name}'")
        print(f"  Shared networks:        {sorted(network_overlap(a, b))}")
        print(f"  Only in {a.region_name}: {sorted(networks_only_in(a, b))}")
        print(f"  Only in {b.region_name}: {sorted(networks_only_in(b, a))}")
        print()

    # Recursion testing: sum total ports across the five biggest regions.
    top_five = by_size[:5]
    print(
        f"recursive_total over top-5 regions = "
        f"{recursive_total(top_five)} ports"
    )
