import logging

from .const import *
import re
from homeassistant.components.remote import (
    RemoteEntity, 
    ATTR_CURRENT_ACTIVITY, 
    ATTR_ACTIVITY_LIST, 
    ATTR_ACTIVITY, 
    SERVICE_SEND_COMMAND, 
    SERVICE_LEARN_COMMAND, 
    SERVICE_DELETE_COMMAND, 
    Iterable
)
from typing import Any

from .device import EntityBase, async_setup

from homeassistant.const import ATTR_SUPPORTED_FEATURES, SERVICE_TURN_ON, SERVICE_TURN_OFF, SERVICE_TOGGLE

_LOGGER = logging.getLogger(__name__)

PLATFORM = "remote"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, RemoteEntity):

    # platform property ##############################################################################
    @property
    def current_activity(self) -> str | None:
        return self._attributes.get(ATTR_CURRENT_ACTIVITY)

    @property
    def activity_list(self) -> list[str] | None:
        return self._attributes.get(ATTR_ACTIVITY_LIST)

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else 0

    # method #########################################################################################
    def turn_on(self, **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity, ATTR_ACTIVITY : kwargs[ATTR_ACTIVITY]}, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity, ATTR_ACTIVITY : kwargs[ATTR_ACTIVITY]}, False)


    def turn_off(self, **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    async def async_turn_off(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    
    async def async_toggle(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TOGGLE, {
                                        "entity_id": self._origin_entity}, False)

    def send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_SEND_COMMAND, {
                                        "entity_id": self._origin_entity, "command" : command}, False)

    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_SEND_COMMAND, {
                                        "entity_id": self._origin_entity, "command" : command}, False)

    def learn_command(self, **kwargs: Any) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_LEARN_COMMAND, {
                                        "entity_id": self._origin_entity, **kwargs}, False)

    async def async_learn_command(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_LEARN_COMMAND, {
                                        "entity_id": self._origin_entity, **kwargs}, False)

    async def async_delete_command(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_DELETE_COMMAND, {
                                        "entity_id": self._origin_entity, **kwargs}, False)

