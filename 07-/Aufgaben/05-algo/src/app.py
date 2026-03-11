__title__ = "Flight_Radar"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
The application is designed to fetch and show the traffic-data for multiple airports. 
"""
import time
from pprint import pprint
from fetch_service import FlightClient
from db_storage import FlightStorage

def main() -> None:
    flight = FlightClient("config.json")
    storage = FlightStorage("flights.db")
    airports = flight.config["api"]["airports"]

    for airport in airports:
        rows = flight.fetch_flights(airport)
        records = flight.transform_flights(rows, airport)

        print(f"\n--- {airport} ---")
        for record in records:
            pprint(record)

        storage.add_flights(records)

        time.sleep(2)


if __name__ == "__main__":
    main()