"""DVLA Coordinator."""
from datetime import timedelta
import logging
from homeassistant.const import (
    CONF_API_KEY,
    CONTENT_TYPE_JSON,
)
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import HOST, CONF_REG_NUMBER

_LOGGER = logging.getLogger(__name__)


class DVLACoordinator(DataUpdateCoordinator):
    """Data coordinator."""

    def __init__(self, hass, session, data):
        """Initialize coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="DVLA",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=21600),
        )
        self.session = session
        self.api_key = data[CONF_API_KEY]
        self.reg_number = str(data[CONF_REG_NUMBER]).upper()

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            resp = await self.session.request(
                method="POST",
                url=HOST,
                headers={
                    "Content-Type": CONTENT_TYPE_JSON,
                    "x-api-key": self.api_key,
                },
                json={"registrationNumber": self.reg_number},
            )
            body = await resp.json()
        except InvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except DVLAError as err:
            raise UpdateFailed(str(err)) from err
        except ValueError as err:
            err_str = str(err)

            if "Invalid authentication credentials" in err_str:
                raise InvalidAuth from err
            if "API rate limit exceeded." in err_str:
                raise APIRatelimitExceeded from err

            _LOGGER.exception("Unexpected exception")
            raise UnknownError from err

        if "errors" in body:
            error = body["errors"][0]
            raise UnknownError(
                f"Error setting up {self.reg_number}: {error['title']}({error['code']}) - {error['detail']}"
            )

        if "message" in body:
            raise UnknownError(f"Error setting up {self.reg_number}: {body['message']}")

        return body


class DVLAError(HomeAssistantError):
    """Base error."""


class InvalidAuth(DVLAError):
    """Raised when invalid authentication credentials are provided."""


class APIRatelimitExceeded(DVLAError):
    """Raised when the API rate limit is exceeded."""


class UnknownError(DVLAError):
    """Raised when an unknown error occurs."""
