"""API client for Meteo.lt."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import aiohttp
import async_timeout

from .const import (
    API_BASE_URL,
    API_PLACES_ENDPOINT,
    API_FORECASTS_ENDPOINT,
)

_LOGGER = logging.getLogger(__name__)


class MeteoLTApiError(Exception):
    """General API error."""


class MeteoLTApiClient:
    """API client for Meteo.lt."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        place_code: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._place_code = place_code

    async def async_get_data(self) -> Dict[str, Any]:
        """Get data from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(
                    f"{API_BASE_URL}{API_PLACES_ENDPOINT}/{self._place_code}{API_FORECASTS_ENDPOINT}"
                )
                response.raise_for_status()
                data = await response.json()

                return data

        except asyncio.TimeoutError as exception:
            raise MeteoLTApiError("Timeout error fetching data") from exception
        except (aiohttp.ClientError, aiohttp.ContentTypeError) as exception:
            raise MeteoLTApiError("Error fetching data") from exception

    async def async_get_places(self) -> List[Dict[str, Any]]:
        """Get list of available places."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(
                    f"{API_BASE_URL}{API_PLACES_ENDPOINT}"
                )
                response.raise_for_status()

                # Filter only Lithuanian locations
                places = await response.json()
                return [place for place in places if place["countryCode"] == "LT"]

        except asyncio.TimeoutError as exception:
            raise MeteoLTApiError(
                "Timeout error fetching places") from exception
        except (aiohttp.ClientError, aiohttp.ContentTypeError) as exception:
            raise MeteoLTApiError("Error fetching places") from exception
