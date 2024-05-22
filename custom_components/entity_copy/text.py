import logging

from .const import *
import re
from homeassistant.components.text import ATTR_MIN, ATTR_MAX, SERVICE_SET_VALUE, ATTR_PATTERN, ATTR_VALUE, TextEntity, TextMode

from .device import EntityBase, async_setup

from homeassistant.const import ATTR_MODE

_LOGGER = logging.getLogger(__name__)

PLATFORM = "text"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, TextEntity):

    # platform property ##############################################################################
    @property
    def mode(self) -> TextMode:
        return self._attributes.get(ATTR_MODE)
    
    @property
    def native_max(self) -> int:
        return self._attributes.get(ATTR_MAX) if self._attributes.get(ATTR_MIN) != None else 0

    @property
    def native_min(self) -> int:
        return self._attributes.get(ATTR_MIN) if self._attributes.get(ATTR_MIN) != None else 0

    @property
    def pattern(self) -> str | None:
        return self._attributes.get(ATTR_PATTERN)

    @property
    def native_value(self) -> str | None:
        return self.state


    # method #########################################################################################
    async def async_set_value(self, value: str) -> None:
        if re.search("^input_text.", self._origin_entity):
            return await self.hass.services.async_call('input_text', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, ATTR_VALUE: value }, False)
        elif re.search("^text.", self._origin_entity):
            return await self.hass.services.async_call('text', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, ATTR_VALUE: value }, False)

    def set_value(self, value: str) -> None:
        if re.search("^input_text.", self._origin_entity):
            return self.hass.services.call('input_text', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, ATTR_VALUE: value }, False)
        elif re.search("^text.", self._origin_entity):
            return self.hass.services.call('text', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, ATTR_VALUE: value }, False)