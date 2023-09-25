import logging

from .const import *
import re
from homeassistant.components.cover import CoverEntity, ATTR_CURRENT_POSITION, ATTR_CURRENT_TILT_POSITION, ATTR_POSITION, ATTR_TILT_POSITION, STATE_CLOSING, STATE_CLOSED,CoverEntityFeature

from .device import EntityBase, async_setup

from homeassistant.const import *
from typing import Any

_LOGGER = logging.getLogger(__name__)

PLATFORM = "cover"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, CoverEntity):

    # platform property #############################################################################
    @property
    def current_cover_position(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_POSITION)
    
    @property
    def current_cover_tilt_position(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_TILT_POSITION)
    
    @property
    def is_opening(self) -> bool | None:
        return self._state == STATE_OPENING
    
    @property
    def is_closing(self) -> bool | None:
        return self._state == STATE_CLOSING

    @property
    def is_closed(self) -> bool | None:
        return self._state == STATE_CLOSED

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get("supported_features") if self._attributes.get("supported_features") != None else CoverEntityFeature.OPEN

    # method ########################################################################################
    async def async_open_cover(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_OPEN_COVER, {
                                "entity_id": self._origin_entity}, False)

    def open_cover(self, **kwargs):
        """Open the cover."""
        return self.hass.services.call(PLATFORM, SERVICE_OPEN_COVER, {
                                "entity_id": self._origin_entity}, False)

    async def async_close_cover(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_CLOSE_COVER, {
                                "entity_id": self._origin_entity}, False)

    def close_cover(self, **kwargs):
        """Close cover."""
        return self.hass.services.call(PLATFORM, SERVICE_CLOSE_COVER, {
                                "entity_id": self._origin_entity}, False)

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_CLOSE_COVER, {
                                "entity_id": self._origin_entity, ATTR_POSITION : kwargs[ATTR_POSITION] }, False)

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        return self.hass.services.call(PLATFORM, SERVICE_CLOSE_COVER, {
                                "entity_id": self._origin_entity, ATTR_POSITION : kwargs[ATTR_POSITION] }, False)

    async def async_stop_cover(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_STOP_COVER, {
                                "entity_id": self._origin_entity}, False)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        return self.hass.services.call(PLATFORM, SERVICE_STOP_COVER, {
                                "entity_id": self._origin_entity}, False)

    async def async_open_cover_tilt(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_OPEN_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)
        
    def open_cover_tilt(self, **kwargs):
        """Open the cover tilt."""
        return self.hass.services.call(PLATFORM, SERVICE_OPEN_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)

    async def async_close_cover_tilt(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_CLOSE_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)

    def close_cover_tilt(self, **kwargs):
        """Close the cover tilt."""
        return self.hass.services.call(PLATFORM, SERVICE_CLOSE_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)

    async def async_set_cover_tilt_position(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SET_COVER_TILT_POSITION, {
                                "entity_id": self._origin_entity, ATTR_POSITION : kwargs[ATTR_POSITION] }, False)

    def set_cover_tilt_position(self, **kwargs):
        """Move the cover tilt to a specific position."""
        return self.hass.services.call(PLATFORM, SERVICE_SET_COVER_TILT_POSITION, {
                                "entity_id": self._origin_entity, ATTR_POSITION : kwargs[ATTR_POSITION] }, False)


    async def async_stop_cover_tilt(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_STOP_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)


    def stop_cover_tilt(self, **kwargs):
        """Stop the cover."""
        return self.hass.services.call(PLATFORM, SERVICE_STOP_COVER_TILT, {
                                "entity_id": self._origin_entity}, False)
