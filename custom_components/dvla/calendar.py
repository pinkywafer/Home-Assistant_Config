"""DVLA sensor platform."""
from datetime import timedelta, date, datetime
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN, CONF_REG_NUMBER
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.util.dt import start_of_local_day
from .coordinator import DVLACoordinator
from .sensor import SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

DATE_SENSOR_TYPES = [st for st in SENSOR_TYPES if st.device_class == SensorDeviceClass.DATE]


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

    sensors = [DVLACalendarSensor(coordinator, name)]
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

    sensors = [DVLACalendarSensor(coordinator, name)]
    async_add_entities(sensors, update_before_add=True)


class DVLACalendarSensor(CoordinatorEntity[DVLACoordinator], CalendarEntity):
    """Define an DVLA sensor."""

    def __init__(
        self,
        coordinator: DVLACoordinator,
        name: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{name}")},
            manufacturer=coordinator.data.get("make"),
            name=name.upper(),
            configuration_url="https://github.com/jampez77/DVLA-Vehicle-Checker/",
        )
        self._attr_unique_id = f"{DOMAIN}-{name}-calendar".lower()
        self._attr_name = f"{DOMAIN} - {name}".upper()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return bool(self.coordinator.data)

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        events = self.get_events(datetime.today())
        return sorted(events, key=lambda c: c.start)[0]

    def get_events(self, start_date: datetime) -> list[CalendarEvent]:
        """Return calendar events."""
        events = []
        for date_sensor_type in DATE_SENSOR_TYPES:
            raw_value = self.coordinator.data.get(date_sensor_type.key)
            if not raw_value:
                _LOGGER.warn(f'No date for {date_sensor_type.key}')
                continue
            value = date.fromisoformat(raw_value)
            if value >= start_date.date():
                event_name = date_sensor_type.name.replace(' Date', '')
                events.append(CalendarEvent(value, value, event_name))
        return events

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        events = []
        for event in self.get_events(start_date):
            if event.start <= end_date.date():
                events.append(event)
        return events
