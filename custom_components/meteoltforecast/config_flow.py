"""Config flow for Meteo.lt integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol
from geopy.distance import geodesic
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .api import MeteoLTApiClient, MeteoLTApiError
from .const import DOMAIN, CONF_PLACE, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


async def _get_closest_place(hass: HomeAssistant, places: list[dict]) -> str | None:
    """Get the closest place to home coordinates."""
    if not (home_coord := await hass.async_add_executor_job(
        lambda: hass.config.location_name and (
            hass.config.latitude,
            hass.config.longitude,
        )
    )):
        return None

    closest_place = None
    min_distance = float('inf')

    for place in places:
        place_coord = (
            place["coordinates"]["latitude"],
            place["coordinates"]["longitude"]
        )
        distance = geodesic(home_coord, place_coord).km

        if distance < min_distance:
            min_distance = distance
            closest_place = place["code"]

    return closest_place


class MeteoLTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meteo.lt."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._places: dict[str, str] = {}
        self._default_place: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=self._places.get(user_input[CONF_PLACE], DEFAULT_NAME),
                data=user_input,
            )

        try:
            session = async_get_clientsession(self.hass)
            # Empty place for getting places list
            client = MeteoLTApiClient(session, "")
            places = await client.async_get_places()

            self._places = {
                place["code"]: place["name"]
                for place in places
            }

            # Get closest place to home coordinates
            self._default_place = await _get_closest_place(self.hass, places)

        except MeteoLTApiError:
            errors["base"] = "cannot_connect"
            self._places = {}
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
            self._places = {}

        placeoptions = sorted(
            [(k, v) for k, v in self._places.items()],
            key=lambda x: x[1],  # Sort by name
        )

        # If we have a default place, move it to the top of the list
        if self._default_place and self._default_place in self._places:
            placeoptions.insert(
                0,
                placeoptions.pop(
                    next(
                        i for i, (k, _) in enumerate(placeoptions)
                        if k == self._default_place
                    )
                ),
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_PLACE,
                    default=self._default_place if self._default_place else vol.UNDEFINED
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(
                                value=place_id, label=place_name
                            )
                            for place_id, place_name in placeoptions
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Meteo.lt integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
