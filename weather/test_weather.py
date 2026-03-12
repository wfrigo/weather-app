"""
test_weather.py - Unit tests for the weather app.

Run with:
    python -m pytest test_weather.py -v
  or:
    python -m unittest test_weather -v

Key concept: MOCKING
  Our functions call requests.get() to hit real APIs.
  In tests we don't want real network calls — they're slow and unreliable.
  We use unittest.mock.patch to replace requests.get with a fake function
  that returns whatever response we tell it to.
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

import api
import display


# ---------------------------------------------------------------------------
# Helpers — fake API responses we'll reuse across tests
# ---------------------------------------------------------------------------

def make_mock_response(json_data: dict, status_code: int = 200) -> MagicMock:
    """
    Build a fake requests.Response object.

    MagicMock lets us create an object that mimics any real object.
    We set .json() to return our fake data and raise_for_status() to do nothing.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data  # .json() will return this dict
    mock_resp.raise_for_status.return_value = None  # do nothing (no error)
    return mock_resp


FAKE_GEO_RESPONSE = {
    "results": [
        {
            "name": "London",
            "country": "United Kingdom",
            "latitude": 51.5085,
            "longitude": -0.1257,
        }
    ]
}

FAKE_WEATHER_RESPONSE = {
    "current": {
        "temperature_2m": 10.5,
        "apparent_temperature": 8.0,
        "weathercode": 3,
        "windspeed_10m": 20.0,
        "relative_humidity_2m": 70,
    },
    "daily": {
        "time": ["2026-03-11", "2026-03-12"],
        "weathercode": [61, 0],
        "temperature_2m_max": [13.0, 15.0],
        "temperature_2m_min": [7.0, 9.0],
    },
}


# ---------------------------------------------------------------------------
# Tests for api.py
# ---------------------------------------------------------------------------

class TestGetCoordinates(unittest.TestCase):

    @patch("api.requests.get")  # replace requests.get inside the api module
    def test_returns_location_for_valid_city(self, mock_get):
        """Happy path: valid city name returns a location dict."""
        mock_get.return_value = make_mock_response(FAKE_GEO_RESPONSE)

        result = api.get_coordinates("London")

        self.assertEqual(result["name"], "London")
        self.assertEqual(result["country"], "United Kingdom")
        self.assertAlmostEqual(result["latitude"], 51.5085)
        self.assertAlmostEqual(result["longitude"], -0.1257)

    @patch("api.requests.get")
    def test_returns_none_for_unknown_city(self, mock_get):
        """If the API returns no results, the function should return None."""
        mock_get.return_value = make_mock_response({"results": []})

        result = api.get_coordinates("NotARealCity123")

        self.assertIsNone(result)

    @patch("api.requests.get")
    def test_returns_none_when_results_key_missing(self, mock_get):
        """If the API returns an empty object, the function should return None."""
        mock_get.return_value = make_mock_response({})

        result = api.get_coordinates("Nowhere")

        self.assertIsNone(result)

    @patch("api.requests.get")
    def test_calls_correct_url(self, mock_get):
        """Verify we're hitting the right endpoint with the city name."""
        mock_get.return_value = make_mock_response(FAKE_GEO_RESPONSE)

        api.get_coordinates("London")

        # mock_get.call_args holds the arguments the function was called with
        args, kwargs = mock_get.call_args
        self.assertIn("geocoding-api.open-meteo.com", args[0])
        self.assertEqual(kwargs["params"]["name"], "London")


class TestGetWeather(unittest.TestCase):

    @patch("api.requests.get")
    def test_returns_current_and_daily(self, mock_get):
        """Weather response should contain 'current' and 'daily' keys."""
        mock_get.return_value = make_mock_response(FAKE_WEATHER_RESPONSE)

        result = api.get_weather(51.5085, -0.1257)

        self.assertIn("current", result)
        self.assertIn("daily", result)

    @patch("api.requests.get")
    def test_current_has_expected_fields(self, mock_get):
        """Current conditions should include temperature and weathercode."""
        mock_get.return_value = make_mock_response(FAKE_WEATHER_RESPONSE)

        result = api.get_weather(51.5085, -0.1257)
        current = result["current"]

        self.assertEqual(current["temperature_2m"], 10.5)
        self.assertEqual(current["weathercode"], 3)

    @patch("api.requests.get")
    def test_calls_correct_url(self, mock_get):
        """Verify we're hitting the forecast endpoint."""
        mock_get.return_value = make_mock_response(FAKE_WEATHER_RESPONSE)

        api.get_weather(51.5085, -0.1257)

        args, _ = mock_get.call_args
        self.assertIn("api.open-meteo.com/v1/forecast", args[0])


# ---------------------------------------------------------------------------
# Tests for display.py
# ---------------------------------------------------------------------------

class TestWeatherDescription(unittest.TestCase):

    def test_known_code_returns_description(self):
        self.assertEqual(display.weather_description(0), "Clear sky")
        self.assertEqual(display.weather_description(61), "Light rain")
        self.assertEqual(display.weather_description(95), "Thunderstorm")

    def test_unknown_code_returns_fallback(self):
        """Codes not in our dict should return a fallback string."""
        result = display.weather_description(999)
        self.assertIn("999", result)  # the code should appear in the output


class TestPrintCurrent(unittest.TestCase):

    def test_output_contains_city_and_temperature(self):
        """
        We capture stdout using patch to check what gets printed
        without actually printing to the terminal during tests.
        """
        location = {"name": "London", "country": "United Kingdom"}
        current = FAKE_WEATHER_RESPONSE["current"]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display.print_current(location, current)
            output = mock_stdout.getvalue()

        self.assertIn("London", output)
        self.assertIn("United Kingdom", output)
        self.assertIn("10.5", output)   # temperature
        self.assertIn("Overcast", output)  # weathercode 3


class TestPrintForecast(unittest.TestCase):

    def test_output_contains_dates_and_temps(self):
        daily = FAKE_WEATHER_RESPONSE["daily"]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display.print_forecast(daily)
            output = mock_stdout.getvalue()

        self.assertIn("2026-03-11", output)
        self.assertIn("2026-03-12", output)
        self.assertIn("13.0", output)   # max temp day 1
        self.assertIn("Clear sky", output)  # weathercode 0 on day 2


if __name__ == "__main__":
    unittest.main()
