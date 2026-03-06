__title__ = "Weather"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
The Application is desingned fetch and show the current weather in a given city
"""
from src.weather_client import Weather

# App.
#
# Idea:
#   - Run program
#   - Pedir input o recorrer ciudades
#   - Client call
#   - Print info (datos limpios)


def main() -> None:
    city = input("Enter the City Name: ")
    weather_client = Weather("config.json")
    temperature, description, sunrise, sunset = weather_client.fetch_weather(city, "en")

    print(f"\n=== Weather in {city} ===")
    print(f"Temperature: {temperature} °C")
    print(f"Description: {description}")
    print(f"Sunrise: {sunrise} (local time)")
    print(f"Sunset: {sunset} (local time)")

if __name__ == "__main__":
    main()
