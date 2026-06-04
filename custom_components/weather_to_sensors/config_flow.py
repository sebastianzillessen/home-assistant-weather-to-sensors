"""Config flow for Weather to Sensors."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .const import CONF_SOURCE, DOMAIN


class WeatherToSensorsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Pick a weather entity to expose as sensors."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            source = user_input[CONF_SOURCE]
            await self.async_set_unique_id(source)
            self._abort_if_unique_id_configured()
            name = user_input.get(CONF_NAME) or self._default_name(source)
            return self.async_create_entry(
                title=name, data={CONF_SOURCE: source, CONF_NAME: name}
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_SOURCE): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="weather")
                ),
                vol.Optional(CONF_NAME): selector.TextSelector(),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    def _default_name(self, source: str) -> str:
        """Derive a device name from the source entity's friendly name."""
        state = self.hass.states.get(source)
        if state and (friendly := state.attributes.get("friendly_name")):
            return str(friendly)
        return source
