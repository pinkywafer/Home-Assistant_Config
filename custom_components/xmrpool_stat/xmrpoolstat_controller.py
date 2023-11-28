"""XMR pool statistics controller"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
import re
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.components.rest.data import RestData
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_interval

from .const import CONF_WALLET, DOMAIN
from .helpers import GetDictValue

_LOGGER = logging.getLogger(__name__)


class XmrPoolStatController:
    """XmrPoolStatController class"""

    def __init__(
        self, hass: HomeAssistant, config_entry: config_entries.ConfigEntry
    ) -> None:
        """Initialize controller"""
        self._lock = asyncio.Lock()
        self._hass = hass
        self._name: str = config_entry.data[CONF_NAME]
        self._scheduledUpdateCallback = None
        resource = (
            "https://web.xmrpool.eu:8119/stats_address?address="
            + config_entry.data[CONF_WALLET]
        )
        self._rest = RestData(
            self._hass,
            "GET",
            resource,
            auth=None,
            headers=None,
            params=None,
            data=None,
            verify_ssl=True,
            encoding='UTF-8',
            ssl_cipher_list='python_default',
        )
        self._statData: Dict[str, Any] = None
        self._workersData: Dict[str, Dict[str, Any]] = None
        self.listeners = []
        self.entity_id = config_entry.entry_id

    async def async_initialize(self) -> None:
        """Async initialization"""
        await self.async_ScheduledUpdate()
        self._scheduledUpdateCallback = async_track_time_interval(
            self._hass, self.async_ScheduledUpdate, timedelta(seconds=30)
        )

    async def async_reset(self) -> bool:
        """Reset dispatchers"""
        for unsub_dispatcher in self.listeners:
            unsub_dispatcher()

        self.listeners = []
        self._scheduledUpdateCallback()  # remove it now
        return True

    @callback
    async def async_ScheduledUpdate(self, _now=None):
        """Trigger update by timer"""
        await self.async_Update()

    async def async_Update(self):
        """Update data"""
        _LOGGER.debug("async_Update({})".format(self._name))
        try:
            await asyncio.wait_for(self._lock.acquire(), timeout=10)
        except:
            _LOGGER.warning("async_Update({} lock failed)".format(self._name))
            return
        try:  # Lock region start
            await self._rest.async_update()

            if self._rest.data is None:
                _LOGGER.info("async_Update({}) - no data received".format(self._name))
                self._statData = None
                self._workersData = None
            else:
                data = json.loads(self._rest.data)
                if "Error" in data:
                    self._statData = None
                    self._workersData = None
                    _LOGGER.info(
                        "async_Update({}) - error received: {}".format(
                            self._name, data["Error"]
                        )
                    )
                else:
                    self._statData = data["stats"]
                    self._workersData = data["perWorkerStats"]

            async_dispatcher_send(self._hass, self.UpdateSignal)
        finally:  # Lock region end
            self._lock.release()

    @property
    def UpdateSignal(self) -> str:
        """New data event"""
        return "{}-update-{}".format(DOMAIN, self._name)

    @property
    def InError(self) -> bool:
        """Is controller in error (no data)?"""
        return self._statData == None

    def GetData(self, worker: str) -> Dict[str, Any]:
        """Get data block corresponding to worker"""
        if self.InError:
            return None
        if worker == None:
            return self._statData
        return GetDictValue(self._workersData, worker)

    def GetValue(self, worker: str, value: str) -> str:
        """Get value for corresponding worker"""
        return GetDictValue(self.GetData(worker), value)
