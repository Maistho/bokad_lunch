from datetime import UTC, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SYSTEM, DOMAIN

CATEGORIES = {
    1: ("Dagens Rätt", "dagens_ratt"),
    3: ("Dagens Grönt", "dagens_gront"),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    restaurant_name = entry.data[CONF_NAME]
    system = entry.data[CONF_SYSTEM]

    async_add_entities(
        [
            BokadLunchSensor(
                coordinator, entry, order, cat_name, cat_key, restaurant_name, system
            )
            for order, (cat_name, cat_key) in CATEGORIES.items()
        ]
    )


class BokadLunchSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sortorder: int,
        cat_name: str,
        cat_key: str,
        restaurant_name: str,
        system: str,
    ):
        super().__init__(coordinator)
        self._sortorder = sortorder
        self._attr_name = f"{restaurant_name} {cat_name}"
        self._attr_unique_id = f"{system}_{cat_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, system)},
            name=restaurant_name,
            manufacturer="Bokad.se",
            model="Lunch Menu",
        )

    @property
    def native_value(self):
        today = datetime.now(tz=UTC).isoformat()
        if not self.coordinator.data:
            return None

        dish = next(
            (
                item
                for item in self.coordinator.data
                if item.get("workday") == today
                and item.get("sortorder") == self._sortorder
            ),
            None,
        )
        if not dish:
            return "Ingen rätt"
        return dish.get("name", "").split(":")[-1].strip().title()

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}

        today = datetime.now(tz=UTC).isoformat()
        dish = next(
            (
                item
                for item in self.coordinator.data
                if item.get("workday") == today
                and item.get("sortorder") == self._sortorder
            ),
            {},
        )
        return {
            "description": dish.get("description", ""),
            "weekly_menu": [
                item
                for item in self.coordinator.data
                if item.get("sortorder") == self._sortorder
            ],
        }
