"""DVLA binary sensor platform."""
from dataclasses import dataclass
from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from typing import Any
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN, CONF_REG_NUMBER
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .coordinator import DVLACoordinator

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)


@dataclass
class DVLABinarySensorEntityDescription(BinarySensorEntityDescription):

    on_value: str | bool = True


SENSOR_TYPES = [
    DVLABinarySensorEntityDescription(
        key="taxStatus",
        name="Taxed",
        icon="mdi:car",
        on_value="Taxed"
    ),
    DVLABinarySensorEntityDescription(
        key="motStatus",
        name="Mot Valid",
        icon="mdi:car",
        on_value="Valid"
    ),
    DVLABinarySensorEntityDescription(
        key="markedForExport",
        name="Marked for Export",
        icon="mdi:export"
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][entry.entry_id]
    # Update our config to include new repos and remove those that have been removed.
    if entry.options:
        config.update(entry.options)

    session = async_get_clientsession(hass)
    coordinator = DVLACoordinator(hass, session, entry.data)

    await coordinator.async_refresh()

    name = entry.data[CONF_REG_NUMBER]

    sensors = [DVLABinarySensor(coordinator, name, description) for description in SENSOR_TYPES]
    async_add_entities(sensors, update_before_add=True)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    _: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    coordinator = DVLACoordinator(hass, session, config)

    name = config[CONF_REG_NUMBER]

    sensors = [DVLABinarySensor(coordinator, name, description) for description in SENSOR_TYPES]
    async_add_entities(sensors, update_before_add=True)


class DVLABinarySensor(CoordinatorEntity[DVLACoordinator], BinarySensorEntity):
    """Define an DVLA sensor."""

    def __init__(
        self,
        coordinator: DVLACoordinator,
        name: str,
        description: DVLABinarySensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{name}")},
            manufacturer=coordinator.data.get("make"),
            name=name.upper(),
            configuration_url="https://github.com/jampez77/DVLA-Vehicle-Checker/",
        )
        self._attr_unique_id = f"{DOMAIN}-{name}-{description.key}-binary".lower()
        self.entity_id = f"binary_sensor.{DOMAIN}_{name}_{description.key}".lower()
        self.attrs: dict[str, Any] = {}
        self.entity_description = description

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return bool(self.coordinator.data)

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        value: str | bool = self.coordinator.data.get(self.entity_description.key, None)

        on_value = self.entity_description.on_value
        if type(on_value) is str:
            return value.casefold() == on_value.casefold()

        return bool(value)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        for key in self.coordinator.data:
            self.attrs[key] = self.coordinator.data[key]
        return self.attrs
