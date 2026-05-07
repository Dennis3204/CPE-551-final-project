"""
charging_station.py

This file defines the ChargingStation class, which is a single record of one EV charging
station from the NREL Alternative Fuel Stations dataset.

Each ChargingStation contains the station's identification info, its location,
its port counts (Level 1, Level 2, DC Fast), and a few small helper methods
used by the rest of the project to compute regin statistics.
"""


class ChargingStation:
    """
    Represents a single EV charging station.

    Attributes:
        station_id   (int)   Unique NREL ID for the station.
        name         (str)   name of the station.
        city         (str)   City the station is located in.
        zip_code     (str)   5-digit ZIP.
        coordinates  (tuple) (latitude, longitude).
        level1       (int)   Number of Level 1 (120 V) ports.
        level2       (int)   Number of Level 2 (240 V) ports.
        dc_fast      (int)   Number of DC Fast Charging ports.
        network      (str)   Charging network operator (e.g. "Tesla").
        access_code  (str)   
        status_code  (str)   Operational status code from NREL ("E" = available).
    """

    def __init__(self, station_id, name, city, zip_code,
                 latitude, longitude, level1, level2, dc_fast,
                 network, access_code, status_code):
        """Store the station's data on the instance."""
        self.station_id = station_id
        self.name = name
        self.city = city
        self.zip_code = zip_code
        self.coordinates = (latitude, longitude)
        self.level1 = level1
        self.level2 = level2
        self.dc_fast = dc_fast
        self.network = network
        self.access_code = access_code
        self.status_code = status_code

    def total_ports(self):
        """Return the total number of charging ports across all levels."""
        return self.level1 + self.level2 + self.dc_fast

    def is_fast_capable(self):
        """Return True if the station has at least one DC Fast port."""
        return self.dc_fast > 0

    def is_public(self):
        """Return True if the station is open to the public."""
        return self.access_code == 'public'

    def __str__(self):
        """Human-friendly one-line summary."""
        return (f"{self.name} ({self.city}, {self.zip_code}) -- "
                f"{self.total_ports()} ports, network: {self.network}")

    def __repr__(self):
        """Concise debugging representation."""
        return (f"ChargingStation(id={self.station_id}, "
                f"name='{self.name}', city='{self.city}', "
                f"ports={self.total_ports()})")

    def __eq__(self, other):
        """Two stations are equal iff they share the same NREL station_id."""
        if not isinstance(other, ChargingStation):
            return False
        return self.station_id == other.station_id

    def __hash__(self):
        #this is needed to allow hashing
        return hash(self.station_id)
