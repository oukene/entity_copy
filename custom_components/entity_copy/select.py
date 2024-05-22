import logging

from .const import *
import re
from homeassistant.components.select import SelectEntity, ATTR_OPTIONS, ATTR_OPTION, SERVICE_SELECT_OPTION

from .device import EntityBase, async_setup

_LOGGER = logging.getLogger(__name__)

PLATFORM = "select"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, SelectEntity):

    # platform property ##############################################################################
    @property
    def current_option(self) -> str | None:
        return self._attributes.get(ATTR_OPTION)
    
    @property
    def options(self) -> list[str]:
        return self._attributes.get(ATTR_OPTIONS)

    # method #########################################################################################
    async def async_select_option(self, option: str) -> None:
        if re.search("^input_select.", self._origin_entity):
            return await self.hass.services.async_call('input_select', SERVICE_SELECT_OPTION, {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)
        elif re.search("^select.", self._origin_entity):
            return await self.hass.services.async_call(PLATFORM, SERVICE_SELECT_OPTION, {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)

    def select_option(self, option: str) -> None:
        if re.search("^input_select.", self._origin_entity):
            return self.hass.services.call('input_select', SERVICE_SELECT_OPTION, {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)
        elif re.search("^select.", self._origin_entity):
            return self.hass.services.call(PLATFORM, SERVICE_SELECT_OPTION, {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)