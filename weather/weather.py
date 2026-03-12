"""
weather.py - Entry point for the weather CLI app.

Usage:
    python weather.py <city>

Example:
    python weather.py London
    python weather.py "New York"
"""

import sys
import api
import display


def main():
    # sys.argv is the list of command-line arguments.
    # sys.argv[0] is always the script name, so we check for a second argument.
    if len(sys.argv) < 2:
        print("Usage: python weather.py <city>")
        print("Example: python weather.py London")
        sys.exit(1)

    # Join all arguments after the script name to support city names with spaces
    city = " ".join(sys.argv[1:])

    print(f"Looking up '{city}'...")

    # Step 1: Get coordinates for the city
    location = api.get_coordinates(city)
    if location is None:
        print(f"Error: Could not find city '{city}'. Please check the spelling.")
        sys.exit(1)

    # Step 2: Fetch weather data using those coordinates
    weather_data = api.get_weather(location["latitude"], location["longitude"])

    # Step 3: Display the results
    display.print_current(location, weather_data["current"])
    display.print_forecast(weather_data["daily"])


if __name__ == "__main__":
    main()
