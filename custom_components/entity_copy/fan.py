import logging

from .const import *
import re
from homeassistant.components.fan import (
    FanEntity,
    ATTR_DIRECTION,
    ATTR_OSCILLATING,
    ATTR_PERCENTAGE,
    ATTR_PERCENTAGE_STEP,
    ATTR_PRESET_MODES,
    ATTR_PRESET_MODE,
    FanEntityFeature,
    SERVICE_SET_DIRECTION,
    SERVICE_SET_PRESET_MODE,
    SERVICE_SET_PERCENTAGE,
    SERVICE_OSCILLATE,
)
from typing import Any
from .device import EntityBase, async_setup

from homeassistant.const import (
    ATTR_SUPPORTED_FEATURES, SERVICE_TURN_ON, SERVICE_TURN_OFF
)

_LOGGER = logging.getLogger(__name__)

PLATFORM = "fan"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, FanEntity):

    # platform property #############################################################################
    @property
    def is_on(self) -> bool | None:
        if self._state == "on":
            return True
        elif self._state == "off":
            return False

    @property
    def current_direction(self) -> str | None:
        return self._attributes.get(ATTR_DIRECTION)

    @property
    def oscillate(self, oscillating: bool) -> None:
        return self._attributes.get(ATTR_OSCILLATING)

    @property
    def percentage(self) -> int | None:
        return self._attributes.get(ATTR_PERCENTAGE)

    @property
    def percentage_step(self) -> float:
        return self._attributes.get(ATTR_PERCENTAGE_STEP)

    @property
    def preset_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_PRESET_MODES)
    
    @property
    def preset_mode(self) -> str | None:
        return self._attributes.get(ATTR_PRESET_MODE)

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else FanEntityFeature.SET_SPEED

    # method ########################################################################################

    async def async_turn_on(self, percentage: int | None = None, preset_mode: str | None = None, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity}, False)

    def turn_on(self, **kwargs) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity}, False)

    async def async_turn_off(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self, **kwargs) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    async def async_set_direction(self, direction: str) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_DIRECTION, {
                                        "entity_id": self._origin_entity, ATTR_DIRECTION : direction }, False)

    def set_direction(self, direction: str) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_SET_DIRECTION, {
                                        "entity_id": self._origin_entity, ATTR_DIRECTION : direction }, False)
    
    async def async_set_preset_mode(self, preset_mode: str) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_PRESET_MODE, {
                                        "entity_id": self._origin_entity, ATTR_PRESET_MODE : preset_mode }, False)
        

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        return self.hass.services.call(PLATFORM, SERVICE_SET_PRESET_MODE, {
                                        "entity_id": self._origin_entity, ATTR_PRESET_MODE : preset_mode }, False)

    async def async_set_percentage(self, percentage: int) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_PERCENTAGE, {
                                        "entity_id": self._origin_entity, ATTR_PERCENTAGE : percentage }, False)

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        return self.hass.services.call(PLATFORM, SERVICE_SET_PERCENTAGE, {
                                        "entity_id": self._origin_entity, ATTR_PERCENTAGE : percentage }, False)

    async def async_oscillate(self, oscillating: bool) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_OSCILLATE, {
                                        "entity_id": self._origin_entity, ATTR_OSCILLATING : oscillating }, False)

    def oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""
        return self.hass.services.call(PLATFORM, SERVICE_OSCILLATE, {
                                        "entity_id": self._origin_entity, ATTR_OSCILLATING : oscillating }, False)