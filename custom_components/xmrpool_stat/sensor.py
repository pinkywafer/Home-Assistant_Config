"""XMR Pool Statistics sensor platform."""

from collections.abc import Awaitable, Iterable, Mapping
import logging
from typing import Any, Dict, Optional

from voluptuous.validators import Switch

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, STATE_UNKNOWN

# from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.typing import StateType

from .const import (
    DATA_CONTROLLER,
    DOMAIN,
)
from .helpers import DefaultTo
from .xmrpoolstat_controller import XmrPoolStatController

_LOGGER = logging.getLogger(__name__)

SETUP_FACTORY = "facktory"
SETUP_ICON = "icon"
SETUP_NAME = "name"
SETUP_UNIT = "unit"
SETUP_KEY = "key"
SETUP_FACTOR = "factor"

_SENSORS: Dict[str, Dict[str, Any]] = {
    "balance": {
        SETUP_NAME: "Balance",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorScaled,
        SETUP_KEY: "balance",
        SETUP_FACTOR: 1e12,
        SETUP_UNIT: "XMR",
        SETUP_ICON: "mdi:bitcoin",
    },
    "hashrate": {
        SETUP_NAME: "Hashrate",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorHashrate,
        SETUP_ICON: "mdi:gauge",
    },
    "hashrate-raw": {
        SETUP_NAME: "Hashrate Raw",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorHashrateRaw,
        SETUP_UNIT: "H/s",
        SETUP_ICON: "mdi:gauge",
    },
    "hashes": {
        SETUP_NAME: "Hashes",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorValue,
        SETUP_KEY: "hashes",
        SETUP_UNIT: "H",
        SETUP_ICON: "mdi:counter",
    },
    "expired": {
        SETUP_NAME: "Expired",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorValue,
        SETUP_KEY: "expired",
        SETUP_UNIT: "H",
        SETUP_ICON: "mdi:counter",
    },
    "invalid": {
        SETUP_NAME: "Invalid",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorValue,
        SETUP_KEY: "invalid",
        SETUP_UNIT: "H",
        SETUP_ICON: "mdi:counter",
    },
    "last-reward": {
        SETUP_NAME: "Last reward",
        SETUP_FACTORY: lambda: XmrPoolStatisticsSensorScaled,
        SETUP_KEY: "last_reward",
        SETUP_FACTOR: 1e12,
        SETUP_UNIT: "XMR",
        SETUP_ICON: "mdi:bitcoin",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, configEntry: config_entries.ConfigEntry, async_add_entities
):
    """Set up XMR pool statistics sensor."""
    _LOGGER.debug(
        "async_setup_entry({0}), state: {1}".format(
            configEntry.data[CONF_NAME], configEntry.state
        )
    )

    instanceName: str = configEntry.data[CONF_NAME]
    controller: XmrPoolStatController = hass.data[DOMAIN][DATA_CONTROLLER][
        configEntry.entry_id
    ]
    sensors = {}

    @callback
    def controllerUpdatedCallback():
        """Update the values of the controller."""
        UpdateItems(instanceName, controller, async_add_entities, sensors)

    controller.listeners.append(
        async_dispatcher_connect(
            hass, controller.UpdateSignal, controllerUpdatedCallback
        )
    )


@callback
def UpdateItems(
    instanceName: str,
    controller: XmrPoolStatController,
    async_add_entities,
    sensors: Dict[str, Any],
) -> None:
    """Update sensor state"""
    _LOGGER.debug("UpdateItems({})".format(instanceName))
    sensorsToAdd: Dict[str, Any] = []

    for sensor in _SENSORS:
        sensorId = "{}-{}".format(instanceName, sensor)
        if sensorId in sensors:
            if sensors[sensorId].enabled:
                sensors[sensorId].async_schedule_update_ha_state()
        else:
            sensorDefinition = _SENSORS[sensor]
            sensorFactory = sensorDefinition[SETUP_FACTORY]()
            sensorInstance = sensorFactory(
                instanceName, sensor, controller, sensorDefinition
            )
            sensors[sensorId] = sensorInstance
            sensorsToAdd.append(sensorInstance)
    if sensorsToAdd:
        async_add_entities(sensorsToAdd, True)


################################################
class XmrPoolStatisticsSensor(SensorEntity):
    """Define XMR Pool sensor"""

    def __init__(
        self,
        instanceName: str,
        sensorName: str,
        controller: XmrPoolStatController,
        sensorDefinition: Dict[str, Any],
    ) -> None:
        """Initialize"""
        self._instanceName = instanceName
        self._sensorName = sensorName
        self._controller = controller
        self._name = "{} {}".format(
            self._instanceName,
            DefaultTo(sensorDefinition.get(SETUP_NAME), self._sensorName),
        )
        self._icon = sensorDefinition.get(SETUP_ICON)
        self._unit = sensorDefinition.get(SETUP_UNIT)
        self._sensorDefinition = sensorDefinition
        self._privateInit()

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._controller.entity_id + self._sensorName

    @property
    def name(self) -> str:
        """Return name"""
        return self._name

    @property
    def state(self) -> StateType:
        """Return the state."""
        if self._controller.InError:
            return STATE_UNKNOWN
        else:
            return self._stateInternal

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    @property
    def icon(self) -> str:
        """Return the icon."""
        return self._icon

    async def async_update(self):
        """Synchronize state with controller."""
        _LOGGER.debug("async_update")
        # self._val = randint(800, 1200)

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        _LOGGER.debug("async_added_to_hass({})".format(self.name))

    ### Overrides
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        return "OK"

    def _privateInit(self) -> None:
        """Private instance intialization"""
        pass


################################################
class XmrPoolStatisticsSensorHashrate(XmrPoolStatisticsSensor):
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        if self._value == None:
            return STATE_UNKNOWN
        return self._value[0]

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        if self._unit != None:
            return self._unit
        if self._value == None:
            return None
        return self._value[1]

    async def async_update(self):
        """Synchronize state with controller."""
        _LOGGER.debug("XmrPoolStatisticsSensorHashrate.async_update")
        value = self._controller.GetValue(None, "hashrate")
        if value is not None:
            self._value = value.split()
        else:
            self._value = ['0', 'H']

    def _privateInit(self) -> None:
        """Private instance intialization"""
        self._value = None


################################################
class XmrPoolStatisticsSensorHashrateRaw(XmrPoolStatisticsSensorHashrate):
    @property
    def _stateInternal(self) -> StateType:
        """Return the internal state."""
        if self._value == None:
            return STATE_UNKNOWN
        multiplier = 0.0
        unit = self._value[1]
        if unit == "H":
            multiplier = 1000.0
        elif unit == "KH":
            multiplier = 1000.0
        elif unit == "MH":
            multiplier = 1000000.0
        return int(float(self._value[0]) * multiplier)


################################################
class XmrPoolStatisticsSensorValue(XmrPoolStatisticsSensor):
    @property
    def _stateInternal(self) -> StateType:
        return self._controller.GetValue(None, self._key)

    def _privateInit(self) -> None:
        """Private instance intialization"""
        self._key: str = self._sensorDefinition[SETUP_KEY]


################################################
class XmrPoolStatisticsSensorScaled(XmrPoolStatisticsSensorValue):
    @property
    def _stateInternal(self) -> StateType:
        return float(self._controller.GetValue(None, self._key)) / self._factor

    def _privateInit(self) -> None:
        """Private instance intialization"""
        super()._privateInit()
        self._factor: float = self._sensorDefinition[SETUP_FACTOR]


#   @property
#   def device_info(self) -> Dict[str, Any]:
#       """Return a description for device registry."""
#       info = {
#           "name": "test",
#           "identifiers": {
#               (
#                   DOMAIN,
#                   self._instanceName,
#               )
#           },
#       }
#
#       return info
