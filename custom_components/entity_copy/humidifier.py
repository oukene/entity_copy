import logging

from .const import *
import re
from homeassistant.components.humidifier import (
    HumidifierEntity,
    ATTR_HUMIDITY,
    ATTR_CURRENT_HUMIDITY,
    ATTR_MAX_HUMIDITY,
    DEFAULT_MAX_HUMIDITY,
    ATTR_MIN_HUMIDITY,
    DEFAULT_MIN_HUMIDITY,
    ATTR_AVAILABLE_MODES,
    HumidifierAction,
    ATTR_ACTION,
    SERVICE_SET_MODE,
    SERVICE_SET_HUMIDITY
)
from typing import Any
from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "humidifier"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, HumidifierEntity):

    # platform property ##############################################################################
    @property
    def target_humidity(self) -> int | None:
        return self._attributes.get(ATTR_HUMIDITY)

    @property
    def current_humidity(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_HUMIDITY)

    @property
    def max_humidity(self) -> int:
        return self._attributes.get(ATTR_MAX_HUMIDITY) if self._attributes.get(ATTR_MAX_HUMIDITY) != None else DEFAULT_MAX_HUMIDITY

    @property
    def min_humidity(self) -> int:
        return self._attributes.get(ATTR_MIN_HUMIDITY) if self._attributes.get(ATTR_MIN_HUMIDITY) != None else DEFAULT_MIN_HUMIDITY
    
    @property
    def mode(self) -> str | None:
        return self._attributes.get(ATTR_MODE)

    @property
    def available_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_AVAILABLE_MODES)

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else 0

    @property
    def is_on(self) -> bool | None:
        return self._state == STATE_ON

    @property
    def device_class(self):
        return self._attributes.get(ATTR_DEVICE_CLASS)

    @property
    def action(self) -> HumidifierAction | None:
        return self._attributes.get(ATTR_ACTION)
        

    # method #########################################################################################

    def turn_on(self, **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity, **kwargs}, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity, **kwargs}, False)


    def turn_off(self, **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    async def async_turn_off(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    def set_mode(self, mode: str) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_SET_MODE, {
                                        "entity_id": self._origin_entity, ATTR_MODE: mode }, False)

    async def async_set_mode(self, mode: str) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_MODE, {
                                        "entity_id": self._origin_entity, ATTR_MODE: mode }, False)


    def set_humidity(self, humidity: int) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_SET_HUMIDITY, {
                                        "entity_id": self._origin_entity, ATTR_HUMIDITY: humidity }, False)

    async def async_set_humidity(self, humidity: int) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_HUMIDITY, {
                                        "entity_id": self._origin_entity, ATTR_HUMIDITY: humidity }, False)
