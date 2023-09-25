import logging

from .const import *
import re
from homeassistant.components.number import *
from homeassistant.components.number import SERVICE_SET_VALUE

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "number"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, NumberEntity):
    # platform property ##############################################################################
    @property
    def native_value(self):
        """Return the state of the sensor."""
        # return self._state
        return self._state
    
    @property
    def native_max_value(self) -> float:
        return self._attributes.get(ATTR_MAX) if self._attributes.get(ATTR_MAX) != None else DEFAULT_MAX_VALUE

    @property
    def native_min_value(self) -> float:
        return self._attributes.get(ATTR_MIN) if self._attributes.get(ATTR_MIN) != None else DEFAULT_MIN_VALUE

    @property
    def native_step(self) -> float:
        return self._attributes.get(ATTR_STEP) if self._attributes.get(ATTR_STEP) != None else DEFAULT_STEP

    @property
    def mode(self) -> NumberMode:
        return self._attributes.get(ATTR_MODE)

    # method #########################################################################################

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.debug("call set native value")
        if re.search("^input_number.", self._origin_entity):
            _LOGGER.debug("call input_number")
            return await self.hass.services.async_call('input_number', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, "value" : value }, False)
        elif re.search("^number.", self._origin_entity):
            _LOGGER.debug("call number")
            return await self.hass.services.async_call(PLATFORM, SERVICE_SET_VALUE, {
                                        "entity_id": self._origin_entity, "value" : value }, False)
                                        
    def set_native_value(self, value: float) -> None:
        _LOGGER.debug("call set native value")
        if re.search("^input_number.", self._origin_entity):
            _LOGGER.debug("call input_number")
            return self.hass.services.call('input_number', SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, "value" : value }, False)
        elif re.search("^number.", self._origin_entity):
            _LOGGER.debug("call number")
            return self.hass.services.call(PLATFORM, SERVICE_SET_VALUE, {
                                            "entity_id": self._origin_entity, "value" : value }, False)

