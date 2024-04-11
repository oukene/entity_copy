import logging

from .const import *
import re
from homeassistant.components.sensor import SensorEntity

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "sensor"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, SensorEntity):

    # platform property ##############################################################################
    @property
    def native_value(self):
        """Return the state of the sensor."""
        # return self._state
        return self._state

    # method #########################################################################################
    def update(self):
        """Update the state."""

