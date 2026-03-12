# Weather CLI

A command-line weather app built in Python to practice working with APIs.

Fetches real-time weather and a 7-day forecast for any city using the [Open-Meteo](https://open-meteo.com/) API — no API key required.

## Features

- Current conditions: temperature, feels like, humidity, wind speed
- 7-day daily forecast with highs and lows
- Automatic timezone detection

## Requirements

- Python 3.10+
- `requests` library

```bash
pip install requests
```

## Usage

```bash
python weather.py <city>
```

**Examples:**

```bash
python weather.py London
python weather.py "New York"
python weather.py Tokyo
```

**Sample output:**

```
========================================
  Weather in London, United Kingdom
========================================
  Condition:    Clear sky
  Temperature:  9.4°C
  Feels like:   5.3°C
  Humidity:     61%
  Wind speed:   16.6 km/h

  7-Day Forecast:
  ------------------------------------
  2026-03-11  Drizzle                  8.1°C / 12.9°C
  2026-03-12  Light drizzle            7.3°C / 11.5°C
  ...
```

## Project Structure

```
weather/
├── weather.py      # Entry point, CLI argument handling
├── api.py          # API calls (geocoding + weather)
├── display.py      # Output formatting
└── test_weather.py # Unit tests
```

## Running Tests

```bash
cd weather
python -m unittest test_weather -v
```

## APIs Used

| API | Purpose |
|-----|---------|
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | Convert city name to coordinates |
| [Open-Meteo Forecast](https://open-meteo.com/en/docs) | Fetch weather data |