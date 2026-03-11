import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from data_transform import FlightRecord

# Fetch + send (to Main) information about arrival flights in a determinate airport.
#
# Idea:
#   - Leer config
#   - Cargar API KEY
#   - Fetch flight data
#   - Transformar a JSON
#   - Devolver info (datos limpios)
#

@dataclass
class FlightClient:
    """
    config + env + API-request
    """
    def __init__(self, config_path: str) -> None:
        self.project_root = Path(__file__).parent
        self.config = self._load_config(config_path)
       # self.logger = self._setup_logging(self.config)

        env_path = self.project_root / ".env"
        load_dotenv(env_path)

        self.api_key = os.getenv("API_KEY_RAPID")
        if not self.api_key:
            raise RuntimeError("Missing API_KEY_RAPID in .env")

        # self.logger.info("Flight client initialized.")
        # self.logger.info("Logger test message")

    def _load_config(self, config_path: str) -> dict:
        """
        Load JSON from configuration.
        """
        cfg_path = (self.project_root / config_path).resolve()
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config not found: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)


    def fetch_flights(self, iata_airport: str) -> list[FlightRecord]:

        api_config = self.config.get("api", {}) #
        base_url = api_config["base_url"] #
        timeout = api_config.get("timeout_seconds", 1200) #

        range_hours = api_config.get("range_hours", 6)

        now = datetime.now()
        end_date = now + timedelta(hours=range_hours)

        start = now.strftime("%Y-%m-%dT%H:%M")
        end = end_date.strftime("%Y-%m-%dT%H:%M")

        url = f"{base_url}/iata/{iata_airport}/{start}/{end}"

        querystring = {
            "withLeg": str(api_config.get("withLeg", True)).lower(),
            "direction": api_config.get("direction", "Arrival"),
            "withCancelled": str(api_config.get("withCancelled", False)).lower(),
            "withCodeshared": str(api_config.get("withCodeshared", True)).lower(),
            "withCargo": str(api_config.get("withCargo", False)).lower(),
            "withPrivate": str(api_config.get("withPrivate", False)).lower(),
            "withLocation": str(api_config.get("withLocation", False)).lower(),
        }

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=timeout)
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code

            if status_code == 429:
                print("Rate limit reached: too many requests to the API.")
            else:
                print(f"HTTP error: {status_code}")
                print(f"Body: {e.response.text}")
            raise

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise

        return data.get("arrivals", [])


    @staticmethod
    def transform_flights(raw_flights: list[dict], destination_airport:str) -> list[FlightRecord]:
        """
        Convert raw flight data into FlightRecord objects ready for SQLite.
        """
        records = []

        for flight in raw_flights:
            origin_country = flight.get("departure", {}).get("airport", {}).get("countryCode")
            origin_iata_airport = flight.get("departure", {}).get("airport", {}).get("iata")
            destination_airport = destination_airport
            flight_number = flight.get("number")
            airline = flight.get("airline", {}).get("name")
            arrival_info = flight.get("arrival", {}).get("scheduledTime", {}).get("local")

            if not arrival_info:
                continue

            arrival_dt = datetime.fromisoformat(arrival_info)

            year = arrival_dt.year
            month = arrival_dt.month
            day = arrival_dt.day
            hour = arrival_dt.hour
            minute = arrival_dt.minute
            second = arrival_dt.second

            record = FlightRecord(
                origin_country=origin_country,
                origin_iata_airport=origin_iata_airport,
                destination_airport=destination_airport,
                flight_number=flight_number,
                airline_name=airline,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second
            )
            records.append(record)

        return records


