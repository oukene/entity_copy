import logging

from .const import *
import re
from homeassistant.components.binary_sensor import BinarySensorEntity

from .device import EntityBase, async_setup

_LOGGER = logging.getLogger(__name__)

PLATFORM = "binary_sensor"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, BinarySensorEntity):

    # platform property ##############################################################################
    @property
    def is_on(self) -> bool | None:
        if self._state == "on":
            return True
        elif self._state == "off":
            return False

    # method #########################################################################################
    def update(self):
        """Update the state."""

