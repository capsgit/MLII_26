__title__ = "Weather"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
The application is designed to fetch and show the current weather
for multiple cities and languages.
"""

from src.weather_client import Weather


def print_weather_report(city: str, temperature: float, description: str, sunrise: str, sunset: str, lang: str) -> None:
    """
    Print a weather report in a readable format.
    """
    print(f"\n=== Weather in {city} ({lang}) ===")
    print(f"Temperature: {temperature} °C")
    print(f"Description: {description}")
    print(f"Sunrise: {sunrise} (local time)")
    print(f"Sunset: {sunset} (local time)")


def process_all_cities(weather_client: Weather) -> None:
    """
    Fetch and print weather for all configured cities and languages.
    """
    cities = weather_client.config["cities"]
    languages = weather_client.config["api"]["languages"]

    for lang in languages:
        for city in cities:
            try:
                temperature, description, sunrise, sunset = weather_client.fetch_weather(city, lang)
                print_weather_report(city, temperature, description, sunrise, sunset, lang)

            except Exception as e:
                weather_client.logger.error("Failed processing city=%s lang=%s: %s", city, lang, e)


def main() -> None:
    """
    Application entry point.
    """
    weather_client = Weather("config.json")
    process_all_cities(weather_client)


if __name__ == "__main__":
    main()