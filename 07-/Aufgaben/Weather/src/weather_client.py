import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# Fetch + send (to Main) information about a city's weather.
#
# Idea:
#   - Leer config
#   - Cargar API KEY
#   - Fetch weather data
#   - Transformar a JSON
#   - Devolver info (datos limpios)
#


@dataclass
class Weather:
    config_path: str

    def __post_init__(self) -> None:
        self.project_root = Path(__file__).parent.parent
        self.config = self._load_config(self.config_path)
        self.logger = self._setup_logging(self.config)

        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)

        self.api_key = os.getenv("API_KEY_OWM")
        if not self.api_key:
            raise RuntimeError("Missing API_KEY_OWM in .env")

    def _load_config(self, config_path: str) -> dict:
        """
        Carga el JSON de configuración.

        """
        cfg_path = (self.project_root / config_path).resolve()
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config not found: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _setup_logging(cfg: dict[str, Any]) -> logging.Logger:
        """
        Configura logging en base a config.json.
        """
        log_cfg = cfg.get("logging", {})
        level = log_cfg.get("level", "INFO")
        fmt = log_cfg.get("format", "%(levelname)s: %(message)s")

        logging.basicConfig(level=level, format=fmt)
        return logging.getLogger("weather")

    def fetch_weather(self, city_name: str, lang: str) -> tuple[float, str, str, str]:
        """
        Busca el clima actual de una ciudad y devuelve:
        temperatura, descripción, sunrise, sunset
        """

        api_cfg = self.config.get("api", {})
        url = api_cfg.get("base_url", "https://api.openweathermap.org/data/2.5/weather")
        units = api_cfg.get("units", "metric")
        timeout = api_cfg.get("timeout_seconds", 10)

        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric",
            "lang": lang,
        }

        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout:
            self.logger.error("Timeout requesting city=%s lang=%s", city_name, lang)
            raise
        except requests.exceptions.HTTPError:
            self.logger.error("HTTP %s for city=%s lang=%s. Body: %s", response.status_code, city_name, lang, response.text)
            raise
        except requests.exceptions.RequestException as e:
            self.logger.exception("RequestException for city=%s lang=%s: %s", city_name, lang, e)
            raise

        else:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            sunrise_ts = data["sys"]["sunrise"]
            sunset_ts = data["sys"]["sunset"]
            tz_offset = data["timezone"]

            tz = timezone(timedelta(seconds=tz_offset))

            sunrise = datetime.fromtimestamp(sunrise_ts, tz).strftime("%H:%M")
            sunset = datetime.fromtimestamp(sunset_ts, tz).strftime("%H:%M")

            return temperature, description, sunrise, sunset

        finally:
            print("Done")