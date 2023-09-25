import logging

from .const import *
import re
from homeassistant.components.light import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "light"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, LightEntity):

    # platform property #############################################################################
    @property
    def brightness(self) -> int | None:
        return self._attributes.get(ATTR_BRIGHTNESS)
        
    @property
    def color_mode(self) -> ColorMode | str | None:
        return self._attributes.get(ATTR_COLOR_MODE)

    @property
    def color_temp_kelvin(self) -> int | None:
        return self._attributes.get(ATTR_COLOR_TEMP_KELVIN)

    @property
    def effect(self) -> str | None:
        return self._attributes.get(ATTR_EFFECT)

    @property
    def effect_list(self) -> list[str] | None:
        return self._attributes.get(ATTR_EFFECT_LIST)

    @property
    def hs_color(self) -> tuple[float, float] | None:
        return self._attributes.get(ATTR_HS_COLOR)

    @property
    def is_on(self) -> bool | None:
        return self._state == "on"

    @property
    def max_color_temp_kelvin(self) -> int:
        return self._attributes.get(ATTR_MAX_COLOR_TEMP_KELVIN)

    @property
    def min_color_temp_kelvin(self) -> int:
        return self._attributes.get(ATTR_MIN_COLOR_TEMP_KELVIN)

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        return self._attributes.get(ATTR_RGB_COLOR)

    @property
    def rgbw_color(self) -> tuple[int, int, int, int] | None:
        return self._attributes.get(ATTR_RGBW_COLOR)

    @property
    def rgbww_color(self) -> tuple[int, int, int, int, int] | None:
        return self._attributes.get(ATTR_RGBWW_COLOR)

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        return self._attributes.get(ATTR_SUPPORTED_COLOR_MODES)

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else LightEntityFeature.EFFECT

    @property
    def xy_color(self) -> tuple[float, float] | None:
        return self._attributes.get(ATTR_XY_COLOR)
    
    # method ########################################################################################
    def turn_on(self, **kwargs) -> None:
        self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity}, False)
        for key, value in kwargs.items():
            _LOGGER.debug("turn_on key : " + str(key) + ", value : " + str(value))
        for key, value in kwargs.items():
            service_data = { "entity_id" : self._origin_entity }
            service_data[key] = value
            self.hass.services.call('light', 'turn_on', service_data, False)

    async def async_turn_off(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call('light', 'turn_off', {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self, **kwargs) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity}, False)

