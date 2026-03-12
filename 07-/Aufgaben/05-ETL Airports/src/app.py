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
from flight_row_transformer import transform_flights

def main() -> None:
    client = FlightClient("config.json")
    storage = FlightStorage("flights.db")

    airports = client.config["api"]["airports"]

    for airport in airports:
        try:
            raw_flights = client.fetch_flights(airport)

            records, report = transform_flights(raw_flights, airport)

            inserted = storage.add_flights(records)

            print(f"\n--- {airport} ---")
            print(f"Fetched: {report['raw_total']}")
            print(f"Valid: {report['valid_total']}")
            print(f"Skipped: {report['skipped_total']}")
            print(f"Skip reasons: {report['skip_reasons']}")
            print(f"Inserted into DB: {inserted}")

            for record in records[:5]:
                pprint(record)

            time.sleep(2)

        except Exception as e:
            print(f"Error while processing airport {airport}: {e}")
            continue


if __name__ == "__main__":
    main()