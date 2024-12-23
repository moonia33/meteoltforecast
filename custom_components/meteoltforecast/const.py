"""Constants for the Meteo.lt integration."""
from typing import Final

DOMAIN = "meteoltforecast"
ATTRIBUTION = "Data provided by LHMT"

# Configuration
CONF_PLACE = "place"

# Defaults
DEFAULT_NAME = "Meteo.lt Forecast"
DEFAULT_SCAN_INTERVAL = 1800  # 30 minutes
DEFAULT_FORECAST_MODE = "hourly"

# API
API_BASE_URL = "https://api.meteo.lt/v1"
API_PLACES_ENDPOINT = "/places"
API_FORECASTS_ENDPOINT = "/forecasts/long-term"

# Condition Mappings - maps Meteo.lt conditions to HA conditions
CONDITION_MAPPINGS = {
    "clear": "sunny",
    "partly-cloudy": "partlycloudy",
    "variable-cloudiness": "partlycloudy",
    "cloudy-with-sunny-intervals": "partlycloudy",
    "cloudy": "cloudy",
    "rain-showers": "rainy",
    "light-rain-at-times": "rainy",
    "rain-at-times": "rainy",
    "light-rain": "rainy",
    "rain": "rainy",
    "heavy-rain": "pouring",
    "thunder": "lightning",
    "isolated-thunderstorms": "lightning-rainy",
    "thunderstorms": "lightning-rainy",
    "sleet-showers": "snowy-rainy",
    "sleet-at-times": "snowy-rainy",
    "light-sleet": "snowy-rainy",
    "sleet": "snowy-rainy",
    "freezing-rain": "snowy-rainy",
    "hail": "hail",
    "snow-showers": "snowy",
    "light-snow-at-times": "snowy",
    "snow-at-times": "snowy",
    "light-snow": "snowy",
    "snow": "snowy",
    "heavy-snow": "snowy",
    "snowstorm": "snowy",
    "fog": "fog",
    "squall": "lightning-rainy",
    "null": "cloudy"  # Default if no condition provided
}

# HA Weather Attributes
ATTR_FORECAST_TIME = "datetime"
ATTR_FORECAST_TEMP = "temperature"
ATTR_FORECAST_TEMP_LOW = "templow"
ATTR_FORECAST_PRECIPITATION = "precipitation"
ATTR_FORECAST_WIND_SPEED = "wind_speed"
ATTR_FORECAST_WIND_GUST = "wind_gust_speed"
ATTR_FORECAST_WIND_BEARING = "wind_bearing"
ATTR_FORECAST_CONDITION = "condition"
ATTR_FORECAST_PRECIPITATION_PROBABILITY = "precipitation_probability"
ATTR_FORECAST_HUMIDITY = "humidity"
ATTR_FORECAST_PRESSURE = "pressure"
ATTR_FORECAST_CLOUD_COVERAGE = "cloud_coverage"
