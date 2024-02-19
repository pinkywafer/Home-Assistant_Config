import logging
import time

from homeassistant.components.switch import SwitchEntity

from . import TdarrEntity
from .const import DOMAIN, COORDINATOR

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add the Switch from the config."""
    entry = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    
    for key, value in entry.data["nodes"].items():
        sw = Switch(entry, value, config_entry.options)
        async_add_entities([sw], False)

    sw = Switch(entry, entry.data["globalsettings"], config_entry.options)
    async_add_entities([sw], False)

class Switch(TdarrEntity, SwitchEntity):
    """Define the Switch for turning ignition off/on"""

    def __init__(self, coordinator, switch, options):
        if "nodeName" in switch:
            self._device_id = "tdarr_node_" + switch["nodeName"] + "_paused"
        elif "_id" in switch and switch["_id"] == "globalsettings":
            self._device_id = "tdarr_pause_all"
        else:
            self._device_id = "tdarr_node_" + switch["_id"] + "_paused"
        self.switch = switch
        self.coordinator = coordinator
        self._state = None
        # Required for HA 2022.7
        self.coordinator_context = object()

    async def async_turn_on(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.tdarr.pauseNode,
            self.switch["_id"],
            True
        )

        if update == "OK":
            self._state = True
            self.switch["nodePaused"] = True
            self.async_write_ha_state()



           
    async def async_turn_off(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.tdarr.pauseNode,
            self.switch["_id"],
            False
        )

        if update == "OK":
            self._state = False
            self.switch["nodePaused"] = False
            self.async_write_ha_state()


    @property
    def name(self):
        _LOGGER.debug(self.switch)
        if "nodeName" in self.switch:
            return "tdarr_node_" + self.switch["nodeName"] + "_paused"
        elif "_id" in self.switch and self.switch["_id"] == "globalsettings":
            return "tdarr_pause_all"
        else:
            return "tdarr_node_" + self.switch["_id"] + "_paused"


    @property
    def device_id(self):
        return self.device_id

    @property
    def is_on(self):
        if self._state == True:
            self._state = None
            return True
        elif self._state == False:
            self._state = None
            return False
        if  self.switch["_id"] == "globalsettings":
            return self.coordinator.data["globalsettings"]["pauseAllNodes"]
        for key, value in self.coordinator.data["nodes"].items():
            if value["_id"] == self.switch["_id"]:
                return value["nodePaused"]



    @property
    def icon(self):
        return None

    @property
    def extra_state_attributes(self):
        return None