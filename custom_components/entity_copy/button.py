import logging

from .const import *
import re
from homeassistant.components.button import ButtonEntity, SERVICE_PRESS

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "button"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, ButtonEntity):

    # platform property ##############################################################################

    # method #########################################################################################
    async def async_press(self) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_PRESS, {
                                        "entity_id": self._origin_entity}, False)
    def async_press(self):
        """Update the state."""
        return self.hass.services.call(PLATFORM, SERVICE_PRESS, {
                                        "entity_id": self._origin_entity}, False)
