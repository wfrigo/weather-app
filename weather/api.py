"""
api.py - Handles all communication with external APIs.

We use two APIs, both free and requiring no API key:
  1. Open-Meteo Geocoding: converts a city name into lat/lon coordinates
  2. Open-Meteo Weather:   fetches weather data for those coordinates
"""

import requests


def get_coordinates(city_name: str) -> dict | None:
    """
    Look up a city and return its coordinates.

    Returns a dict with keys: name, country, latitude, longitude
    Returns None if the city is not found.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,        # we only want the top result
        "language": "en",
        "format": "json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # raises an error if the request failed

    data = response.json()

    # The API returns a "results" list; if it's empty, city wasn't found
    if not data.get("results"):
        return None

    result = data["results"][0]
    return {
        "name": result["name"],
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
    }


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather and a 7-day daily forecast for the given coordinates.

    Returns a dict with:
      - current:  dict of current conditions
      - daily:    dict of lists (one value per day) for the forecast
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        # Current conditions we want
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "weathercode",
            "windspeed_10m",
            "relative_humidity_2m",
        ],
        # Daily forecast fields
        "daily": [
            "weathercode",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh",
        "timezone": "auto",  # auto-detect timezone from coordinates
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return {
        "current": data["current"],
        "daily": data["daily"],
    }
