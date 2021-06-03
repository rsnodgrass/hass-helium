import asyncio
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ICON,
    ATTR_NAME,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    CONF_URL,
)
from homeassistant.core import callback
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity

from .client import Helium BlockchainClient
from .const import (
    ATTR_ATTRIBUTION,
    ATTR_DESCRIPTION,
    ATTR_LOG_TIMESTAMP,
    ATTRIBUTION,
    CONF_TIMEOUT,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
    ICON_HOTSPOT,
    ICON_WALLET
)

LOG = logging.getLogger(__name__)

DATA_UPDATED = "helium_data_updated"

SCAN_INTERVAL = timedelta(minutes=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_URL): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int
    }
)


async def async_setup_platform(
    hass, config, async_add_entities_callback, discovery_info=None
):
    """Set up the Helium Hotspot sensor integration."""
    url = config.get(CONF_URL)
    name = config.get(CONF_NAME)
    timeout = config.get(CONF_TIMEOUT)

    client = Helium BlockchainClient(url, name=name, timeout=timeout)

    # create the core Helium Hotspot service sensor, which is responsible for updating all other sensors
    sensor = Helium BlockchainServiceSensor(
        hass, config, name, client, async_add_entities_callback
    )
    async_add_entities_callback([sensor], True)


class Helium BlockchainServiceSensor(Entity):
    """Sensor monitoring the Helium Blockchain and updating any related sensors"""

    def __init__(
        self, hass, config, name, helium_client, async_add_entities_callback
    ):
        """Initialize the Helium Hotspot service sensor."""
        self.hass = hass
        self._name = name

        self._managed_sensors = {}
        self._attrs = {ATTR_ATTRIBUTION: ATTRIBUTION, CONF_URL: config.get(CONF_URL)}

        self._helium_client = helium_client
        self._async_add_entities_callback = async_add_entities_callback

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Helium: " + self._name

    @property
    def state(self):
        """Return the log types being tracked in Helium Hotspot."""
        return self._managed_sensors.keys()

    @property
    def icon(self):
        return ICON_HOTSPOT

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        """Get the latest data from the source and updates the state."""

        # trigger an update of this sensor (and all related sensors)
        client = self._helium_client
        soup = await client.async_update()

        # iterate through all the log entries and update sensor states
        timestamp = await client.process_log_entry_callbacks(
            soup, self._update_sensor_callback
        )
        self._attrs[ATTR_LOG_TIMESTAMP] = timestamp

    @property
    def device_state_attributes(self):
        """Return the any state attributes."""
        return self._attrs

    async def get_sensor_entity(self, sensor_type):
        sensor = self._managed_sensors.get(sensor_type, None)
        if sensor:
            return sensor

        name = self._name + " " + config[ATTR_NAME]

        hotspot_id = "1"
        
        sensor = UpdatableSensor(self.hass, hotspot_id, name, config, sensor_type)
        self._managed_sensors[sensor_type] = sensor

        # register sensor with Home Assistant (async callback requires passing to loop)
        self._async_add_entities_callback([sensor], True)

        return sensor

    async def _update_sensor_callback(self, log_type, timestamp, state):
        """Update the sensor with the details from the log entry"""
        sensor = await self.get_sensor_entity(log_type)
        if sensor and sensor.state != state:
            LOG.info(f"{self._name} {log_type}={state} (timestamp={timestamp})")
            sensor.inject_state(state, timestamp)

    @property
    def sensor_names(self):
        return self._managed_sensors.keys()


class UpdatableSensor(RestoreEntity):
    """Representation of a sensor whose state is kept up-to-date by an external data source."""

    def __init__(self, hass, unique_id, name, config, sensor_type):
        """Initialize the sensor."""
        super().__init__()

        self.hass = hass
        self._name = name
        self._config = config
        self._sensor_type = sensor_type
        self._state = None
        self._unique_id = unique_id

        self._attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def should_poll(self):
        return True  # FIXME: get scheduled updates working below

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._config[ATTR_UNIT_OF_MEASUREMENT]

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the any state attributes."""
        return self._attrs

    @property
    def icon(self):
        return self._config["icon"]

    def inject_state(self, state, timestamp):
        state_changed = self._state != state
        self._attrs[ATTR_LOG_TIMESTAMP] = timestamp

        if state_changed:
            self._state = state

            # FIXME: see should_poll
            # notify Home Assistant that the sensor has been updated
            # if (self.hass and self.schedule_update_ha_state):
            #    self.schedule_update_ha_state(True)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        # for this integration, restoring state really doesn't matter right now (but leaving code below in place)
        # Reason: all the sensors are dynamically created based on Helium Hotspot service call, which always returns
        # the latest state as well!
        if self._state:
            return

        # on restart, attempt to restore previous state (SEE COMMENT ABOVE WHY THIS ISN'T USEFUL CURRENTLY)
        # (see https://aarongodfrey.dev/programming/restoring-an-entity-in-home-assistant/)
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state
        LOG.debug(f"Restored sensor {self._name} previous state {self._state}")

        # restore attributes
        if ATTR_LOG_TIMESTAMP in state.attributes:
            self._attrs[ATTR_LOG_TIMESTAMP] = state.attributes[ATTR_LOG_TIMESTAMP]

        async_dispatcher_connect(
            self.hass, DATA_UPDATED, self._schedule_immediate_update
        )

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)