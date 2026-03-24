from dataclasses import dataclass

@dataclass
class FlightRecord:
    """
    a clean "flight" row
    """
    origin_country: str
    origin_iata_airport: str
    destination_airport: str
    flight_number: str
    airline_name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

