"""
region_profile.py

This file defines the RegionProfile class, which is a collection of ChargingStation objects
that share the same geographic region (a county, a ZIP code, a city, etc.).

This RegionProfile is what the rest of the project will use to rank and visualize
thigs like "where are New York's worst EV charging gaps?" There are also helpers like total ports, fast-charger
count, public station list, and the set of unique networks operating in
the region
"""

from src.charging_station import ChargingStation


class RegionProfile:
    """
    this class is a collection of ChargingStation objects that belong to the same geographic region.

    """

    def __init__(self, region_name, region_type):
        """
        intializes an empty RegionProfile.
        """
        self.region_name = region_name
        self.region_type = region_type
        self.stations = []
        self._networks = set()

    def add_station(self, station):
        """
        Append a ChargingStation to this region and record its network.

        Args:
            station (ChargingStation): The station to add
        """
        self.stations.append(station)
        if station.network:
            self._networks.add(station.network)

    def total_stations(self):
        """Return the number of stations currently in this region."""
        return len(self.stations)

    def total_ports(self):
        """
        Return the total number of charging ports across every station
        in the region
        """
        running_total = 0
        for station in self.stations:
            running_total += station.total_ports()
        return running_total

    def public_stations(self):
        """
        Return a list of the publicly accessible stations in this region.
        """
        return [s for s in self.stations if s.is_public()]

    def fast_charger_count(self):
        """
        Return the number of stations in this region that have at least
        one DC Fast charging port.
        """
        count = 0
        for station in self.stations:
            if station.is_fast_capable():
                count += 1
        return count

    def unique_networks(self):
        """
        Return the set of distinct charging-network operators serving
        this region.
        """
        return self._networks

    def __str__(self):
        """
        human readible versin of the class data
        """
        return (
            f"RegionProfile: {self.region_name} ({self.region_type})\n"
            f"  Stations:        {self.total_stations()}\n"
            f"  Total ports:     {self.total_ports()}\n"
            f"  Fast-capable:    {self.fast_charger_count()}\n"
            f"  Public stations: {len(self.public_stations())}\n"
            f"  Networks:        {sorted(self._networks)}"
        )

    def __len__(self):
        """
        Length of a RegionProfile is the number of stations it contains.
        Lets callers write "len(region)" instead of "region.total_stations()".
        """
        return len(self.stations)

    def __add__(self, other):
        """
        Merge two RegionProfiles into a new combined profile.

        This will be useful for "NYC boroughs combined"
        """
        if not isinstance(other, RegionProfile):
            raise TypeError(
                "Can only add RegionProfile to RegionProfile, "
                f"got {type(other).__name__}."
            )

        combined_type = (
            self.region_type if self.region_type == other.region_type
            else "mixed"
        )
        combined = RegionProfile(
            region_name=f"{self.region_name} + {other.region_name}",
            region_type=combined_type,
        )
        for station in self.stations:
            combined.add_station(station)
        for station in other.stations:
            combined.add_station(station)
        return combined
