import logging

from .const import *
import re
from homeassistant.components.siren import SirenEntity
from typing import Any

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "siren"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, SirenEntity):

    # platform property ##############################################################################
    @property
    def is_on(self) -> bool | None:
        return super().is_on

    @property
    def available_tones(self) -> list[int | str] | dict[int, str] | None:
        return super().available_tones

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else 0
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
