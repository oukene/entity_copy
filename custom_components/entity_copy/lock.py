import logging

#from .const import *
import re
from homeassistant.components.lock import LockEntity, ATTR_CHANGED_BY, LockEntityFeature, LockState
from typing import Any
from .device import EntityBase, async_setup

from homeassistant.const import (
    ATTR_CODE_FORMAT, ATTR_SUPPORTED_FEATURES
)

_LOGGER = logging.getLogger(__name__)

PLATFORM = "lock"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, LockEntity):

    # platform property #############################################################################
    @property
    def changed_by(self) -> str | None:
        return self._attributes.get(ATTR_CHANGED_BY)

    @property
    def code_format(self) -> str | None:
        return self._attributes.get(ATTR_CODE_FORMAT)
    
    @property
    def is_locked(self) -> bool | None:
        return self._state == LockState.STATE_LOCKED

    @property
    def is_locking(self) -> bool | None:
        return self._state == LockState.STATE_LOCKING

    @property
    def is_unlocking(self) -> bool | None:
        return self._state == LockState.STATE_UNLOCKING

    @property
    def is_jammed(self) -> bool | None:
        return self._state == LockState.STATE_JAMMED

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else LockEntityFeature.OPEN

    # method ########################################################################################
    async def async_lock(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call('lock', 'lock', {
                                        "entity_id": self._origin_entity}, False)

    def lock(self, **kwargs: Any) -> None:
        self.hass.services.call('lock', 'lock', {
                                        "entity_id": self._origin_entity}, False)

    async def async_unlock(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call('lock', 'unlock', {
                                        "entity_id": self._origin_entity}, False)

    def unlock(self, **kwargs: Any) -> None:
        return self.hass.services.call('lock', 'unlock', {
                                        "entity_id": self._origin_entity}, False)

    async def async_open(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call('lock', 'open', {
                                        "entity_id": self._origin_entity}, False)

    def open(self, **kwargs: Any) -> None:
        return self.hass.services.call('lock', 'open', {
                                        "entity_id": self._origin_entity}, False)

