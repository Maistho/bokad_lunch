from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_URL, CONF_SYSTEM, DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="Stångs Mjärdevi"): str,
        vol.Required(CONF_SYSTEM, default="stangs-mjardevi"): str,
    }
)


class BokadConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors = {}

        if user_input is not None:
            # Set unique_id per system to prevent duplicate setups
            await self.async_set_unique_id(user_input[CONF_SYSTEM].lower())
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            payload = {
                "system": user_input[CONF_SYSTEM],
                "table": "mealofthedays",
                "condition": {},
            }
            try:
                async with session.post(API_URL, json=payload, timeout=10) as resp:
                    if resp.status != 200:
                        errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
