"""Support for Meteo.lt weather service."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util
from datetime import datetime, timedelta
import zoneinfo

from .const import (
    ATTRIBUTION,
    CONDITION_MAPPINGS,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meteo.lt weather based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([MeteoLTWeather(coordinator, entry)], False)


class MeteoLTWeather(CoordinatorEntity, WeatherEntity):
    """Implementation of a Meteo.lt weather condition."""

    _attr_has_entity_name = True
    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meteo.lt weather."""
        super().__init__(coordinator)
        self._config_entry = config_entry

        # Entity properties
        self._attr_unique_id = config_entry.entry_id
        self._attr_has_entity_name = True
        self._attr_name = None  # This will use the name from the config entry for the entity
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": config_entry.title,
            "manufacturer": "LHMT",
            "model": "Weather Forecast",
            "entry_type": DeviceEntryType.SERVICE,
        }

        # Units
        self._attr_native_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_native_pressure_unit = UnitOfPressure.HPA
        self._attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND
        self._attr_native_precipitation_unit = "mm"

        self._attr_attribution = ATTRIBUTION

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        try:
            if not self.coordinator.data:
                return None

            current = self.coordinator.data["forecastTimestamps"][0]
            condition_code = current.get("conditionCode")
            if not condition_code:
                return None

            # Default to cloudy if unknown
            return CONDITION_MAPPINGS.get(condition_code, "cloudy")

        except (KeyError, IndexError):
            return None

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent (feels like) temperature."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["feelsLikeTemperature"]

        except (KeyError, IndexError):
            return None

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["airTemperature"]

        except (KeyError, IndexError):
            return None

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["seaLevelPressure"]

        except (KeyError, IndexError):
            return None

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["relativeHumidity"]

        except (KeyError, IndexError):
            return None

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["windSpeed"]

        except (KeyError, IndexError):
            return None

    @property
    def native_wind_gust_speed(self) -> float | None:
        """Return the wind gust speed."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["windGust"]

        except (KeyError, IndexError):
            return None

    @property
    def wind_bearing(self) -> float | None:
        """Return the wind bearing."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["windDirection"]

        except (KeyError, IndexError):
            return None

    @property
    def cloud_coverage(self) -> float | None:
        """Return the cloud coverage."""
        try:
            if not self.coordinator.data:
                return None

            return self.coordinator.data["forecastTimestamps"][0]["cloudCover"]

        except (KeyError, IndexError):
            return None

    async def async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast."""
        try:
            if not self.coordinator.data:
                return None

            forecast_data: list[Forecast] = []
            now = dt_util.now()

            # Get next hour
            next_hour = now.replace(
                minute=0, second=0, microsecond=0) + timedelta(hours=1)

            for item in self.coordinator.data["forecastTimestamps"]:
                # Parse UTC time and convert to local timezone
                forecast_time = dt_util.parse_datetime(item["forecastTimeUtc"])
                if forecast_time is None:
                    continue

                # Convert to local time
                local_time = forecast_time.astimezone(now.tzinfo)

                # Skip if time is in the past or current hour
                if local_time < next_hour:
                    continue

                forecast_data.append({
                    "datetime": local_time,
                    "native_temperature": item["airTemperature"],
                    "native_apparent_temperature": item["feelsLikeTemperature"],
                    "native_wind_speed": item.get("windSpeed"),
                    "native_wind_gust_speed": item.get("windGust"),
                    "wind_bearing": item.get("windDirection"),
                    "native_pressure": item.get("seaLevelPressure"),
                    "humidity": item.get("relativeHumidity"),
                    "native_precipitation": item.get("totalPrecipitation", 0),
                    "cloud_coverage": item.get("cloudCover"),
                    "condition": CONDITION_MAPPINGS.get(item.get("conditionCode")),
                })

            return forecast_data

        except (KeyError, IndexError):
            return None
