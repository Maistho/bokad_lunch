import logging
from datetime import UTC, datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BokadDataCoordinator(DataUpdateCoordinator):
    """Fetches weekly lunch data via aiohttp."""

    def __init__(self, hass: HomeAssistant, system: str):
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{system}",
            update_interval=timedelta(hours=4),
        )
        self.system = system
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        today = datetime.now(tz=UTC)
        mon = today - timedelta(days=today.weekday())
        sun = mon + timedelta(days=6)

        payload = {
            "system": self.system,
            "table": "mealofthedays",
            "condition": {
                "workday": {"$gte": mon.isoformat(), "$lte": sun.isoformat()}
            },
        }

        try:
            async with self.session.post(API_URL, json=payload) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching Bokad menu: {err}") from err
