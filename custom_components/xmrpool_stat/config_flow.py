"""Config flow to configure XMR Pool wallet component."""

import json
import logging
from typing import Any, Callable, Dict, Optional
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.components.rest.data import RestData
from homeassistant.core import callback

from .const import CONF_WALLET, DOMAIN

_LOGGER = logging.getLogger(__name__)

# ---------------------------
#   configured_instances
# ---------------------------
@callback
def configured_instances(hass, item: str):
    """Return a set of configured instances."""
    return set(entry.data[item] for entry in hass.config_entries.async_entries(DOMAIN))


class ConfigFlowException(Exception):
    """Excepion in config flow occurred."""

    def __init__(self, error: str) -> None:
        self.error = error


AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_WALLET): cv.string,
    }
)


class XmrPoolFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a wallet config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        _LOGGER.debug(f"async_step_user({user_input})")
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                _LOGGER.debug("user_input not None")
                if user_input[CONF_NAME] in configured_instances(self.hass, CONF_NAME):
                    raise ConfigFlowException("name_exists")
                if user_input[CONF_WALLET] in configured_instances(
                    self.hass, CONF_WALLET
                ):
                    raise ConfigFlowException("wallet_exists")

                resource = (
                    "https://web.xmrpool.eu:8119/stats_address?address="
                    + user_input[CONF_WALLET]
                )
                rest = RestData(
                    self.hass,
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
                await rest.async_update()
                if rest.data is None:
                    raise ConfigFlowException("no_answer")
                data = json.loads(rest.data)
                if "error" in data.keys():
                    _LOGGER.debug("Invalid answer: %s", data["error"])
                    raise ConfigFlowException("invalid_answer")
            except ConfigFlowException as ex:
                _LOGGER.warning("Configuration error: %s", ex.error)
                errors["base"] = ex.error
            except:
                _LOGGER.warning("Unexpected exception")
                errors["base"] = "unknown_exception"
                raise
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=self.data
                )

        _LOGGER.debug("Show input form...")
        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )
