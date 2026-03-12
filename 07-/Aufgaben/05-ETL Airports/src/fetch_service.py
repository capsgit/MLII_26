import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

from models import FlightRecord

# Fetch + send (to Main) information about arrival flights in a determinate airport.
#
# Idea:
#   - Read config
#   - Load API KEY
#   - Fetch flight data
#   - Transform to a JSON
#   - Return info (clean data)
#

class FlightClient:
    """
    config + env + API-request
    """
    def __init__(self, config_path: str) -> None:
        self.project_root = Path(__file__).parent
        self.config = self._load_config(config_path)

        env_path = self.project_root / ".env"
        load_dotenv(env_path)

        self.api_key = os.getenv("API_KEY_RAPID")
        if not self.api_key:
            raise RuntimeError("Missing API_KEY_RAPID in .env")

    def _load_config(self, config_path: str) -> dict:
        """
        Load JSON from configuration.
        """
        cfg_path = (self.project_root / config_path).resolve()
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config not found: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def fetch_flights(self, iata_airport: str) -> list[dict]:
        """
        Get information about arrival flights in a determinate airport from the API.
        endpoint: https://aerodatabox.p.rapidapi.com/iata/{iata_airport}/{start}/{end}
        """
        api_config = self.config.get("api", {})
        base_url = api_config["base_url"]
        timeout = api_config.get("timeout_seconds", 1200)
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

            if not response.text.strip():
                print(f"Empty response body for airport {iata_airport}")
                return []

            try:
                data = response.json()

            except ValueError:
                print(f"Non-JSON response for airport {iata_airport}")
                print(f"Status code: {response.status_code}")
                print(f"Response preview: {response.text[:300]}")
                return []


        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code

            if status_code == 429:
                print(f"Rate limit reached for airport {iata_airport}")

            else:
                print(f"HTTP error for airport {iata_airport}: {status_code}")
                print(f"Body: {e.response.text[:300]}")
            return []

        except requests.exceptions.RequestException as e:
            print(f"Request error for airport {iata_airport}: {e}")
            return []

        return data.get("arrivals", [])
