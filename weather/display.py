"""
display.py - Formats and prints weather data to the terminal.

Keeps all the "presentation" logic separate from the API calls.
"""

# WMO Weather Interpretation Codes → human-readable description
# Full list: https://open-meteo.com/en/docs#weathervariables
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail",
}


def weather_description(code: int) -> str:
    """Convert a WMO weather code to a readable string."""
    return WEATHER_CODES.get(code, f"Unknown ({code})")


def print_current(location: dict, current: dict) -> None:
    """Print the current weather conditions."""
    print(f"\n{'='*40}")
    print(f"  Weather in {location['name']}, {location['country']}")
    print(f"{'='*40}")
    print(f"  Condition:    {weather_description(current['weathercode'])}")
    print(f"  Temperature:  {current['temperature_2m']}°C")
    print(f"  Feels like:   {current['apparent_temperature']}°C")
    print(f"  Humidity:     {current['relative_humidity_2m']}%")
    print(f"  Wind speed:   {current['windspeed_10m']} km/h")


def print_forecast(daily: dict) -> None:
    """Print a 7-day daily forecast."""
    print(f"\n  7-Day Forecast:")
    print(f"  {'-'*36}")

    dates = daily["time"]
    codes = daily["weathercode"]
    highs = daily["temperature_2m_max"]
    lows  = daily["temperature_2m_min"]

    for i in range(len(dates)):
        desc = weather_description(codes[i])
        print(f"  {dates[i]}  {desc:<22} {lows[i]:>4}°C / {highs[i]:>4}°C")

    print()
