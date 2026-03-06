__title__ = "Weather"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
The Application is desingned fetch and show the current weather in a given city
"""
from src.weather_client import Weather

# App. Show temperature for 3 Cities in English and German
#
# Idea:
#   - Run program
#   - Load config
#   - Client call
#   - Print info


def main() -> None:
    # city = input("Enter the City Name: ") # || input???
    weather_client = Weather("config.json")

    cities = weather_client.config["cities"]
    languages = weather_client.config["api"]["languages"]

    weather_client.logger.info("Starting weather app")
    weather_client.logger.info("Cities to process: %s", cities)
    weather_client.logger.info("Languages to process: %s", languages)

    for lang in languages:
        print("\n ===========Languages============= \n")

        for city in cities:
            try:
                temperature, description, sunrise, sunset = (
                    weather_client.fetch_weather(city, lang)
                )

                print(f"\n=== Weather in {city} ===")
                print(f"Temperature: {temperature} °C")
                print(f"Description: {description}")
                print(f"Sunrise: {sunrise} (local time)")
                print(f"Sunset: {sunset} (local time) \n \n")

            except Exception as e:
                weather_client.logger.error(
                    "Failed processing city=%s lang=%s: %s", city, lang, e
                )
                print(f"\n=== Weather in {city} ===")
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
