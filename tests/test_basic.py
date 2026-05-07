"""
test_basic.py

two pytest cases that validate the project's main logic:

    - total_ports() on ChargingStation actually sums L1 + L2 + DC Fast
    - underserved_regions() only yields regions whose gap score is
      above the threshold
"""

from src.analysis import underserved_regions
from src.charging_station import ChargingStation
from src.region_profile import RegionProfile


def test_charging_station_total_ports_sums():
    # one station with 1 + 2 + 3 ports should report 6 total
    station = ChargingStation(
        station_id=1,
        name="Test Station",
        city="Albany",
        zip_code="12207",
        latitude=42.65,
        longitude=-73.76,
        level1=1,
        level2=2,
        dc_fast=3,
        network="ChargePoint",
        access_code="public",
        status_code="E",
    )

    assert station.total_ports() == 6


def test_underserved_generator_by_threshold():
    # an empty region scores 1.0 (worst possible gap), so it should
    # always show up above any reasonable threshold and a region full of
    # public DC Fast stations scores low and should be filtered out.
    desert = RegionProfile(region_name="Desert", region_type="city")

    healthy = RegionProfile(region_name="Healthy", region_type="city")
    for i in range(10):
        healthy.add_station(ChargingStation(
            station_id=i,
            name=f"Station {i}",
            city="Healthy",
            zip_code="00000",
            latitude=0.0,
            longitude=0.0,
            level1=0,
            level2=0,
            dc_fast=2,
            network="EVgo",
            access_code="public",
            status_code="E",
        ))

    regions = {"Desert": desert, "Healthy": healthy}
    results = list(underserved_regions(regions, threshold=0.5))
    names = {name for name, _ in results}

    assert "Desert" in names
    assert "Healthy" not in names
