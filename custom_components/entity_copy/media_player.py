import logging

from .const import *
import re
from homeassistant.components.media_player import (
    MediaPlayerEntity, 
    MediaPlayerEntityFeature,
    ATTR_SOUND_MODE,
    ATTR_SOUND_MODE_LIST,
    ATTR_INPUT_SOURCE,
    ATTR_INPUT_SOURCE_LIST,
    ATTR_GROUP_MEMBERS,
    BrowseMedia,
    MediaPlayerEnqueue,
    MediaType,
    ATTR_MEDIA_CONTENT_TYPE,
    ATTR_MEDIA_CONTENT_ID,
    ATTR_MEDIA_ENQUEUE,
    ATTR_MEDIA_ANNOUNCE,
    ATTR_MEDIA_SEEK_POSITION,
    RepeatMode,
    SERVICE_SELECT_SOUND_MODE,
    ATTR_MEDIA_VOLUME_LEVEL,
    ATTR_MEDIA_VOLUME_MUTED,
    SERVICE_CLEAR_PLAYLIST,
    SERVICE_JOIN,
    SERVICE_SELECT_SOURCE,
    ATTR_MEDIA_SHUFFLE,
    SERVICE_UNJOIN
)
from typing import Any
from .device import EntityBase, async_setup
from homeassistant.components import media_source
from homeassistant.components.media_player.browse_media import (
    async_process_play_media_url,
)

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "media_player"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, MediaPlayerEntity):

    # platform property #############################################################################
    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else MediaPlayerEntityFeature.PAUSE

    @property
    def sound_mode(self) -> str | None:
        return self._attributes.get(ATTR_SOUND_MODE)

    @property
    def sound_mode_list(self) -> list[str] | None:
        return self._attributes.get(ATTR_SOUND_MODE_LIST)

    @property
    def source(self) -> str | None:
        return self._attributes.get(ATTR_INPUT_SOURCE)

    @property
    def source_list(self) -> list[str] | None:
        return self._attributes.get(ATTR_INPUT_SOURCE_LIST)

    @property
    def media_image_url(self) -> str | None:
        return self._attributes.get("media_image_url")

    @property
    def media_image_remotely_accessible(self) -> bool:
        return self._attributes.get("media_image_remotely_accessible")

    @property
    def device_class(self):
        return self._attributes.get(ATTR_DEVICE_CLASS)

    @property
    def group_members(self) -> list[str] | None:
        return self._attributes.get(ATTR_GROUP_MEMBERS)

    # method ########################################################################################

    async def async_browse_media(
        self, media_content_type: str | None = None, media_content_id: str | None = None
    ) -> BrowseMedia:
        """Implement the websocket media browsing helper."""
        # If your media player has no own media sources to browse, route all browse commands
        # to the media source integration.
        return await media_source.async_browse_media(
            self.hass,
            media_content_id,
            # This allows filtering content. In this case it will only show audio sources.
            content_filter=lambda item: item.media_content_type.startswith("audio/"),
        )

    async def async_play_media(
        self,
        media_type: str,
        media_id: str,
        enqueue: MediaPlayerEnqueue | None = None,
        announce: bool | None = None, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        if media_source.is_media_source_id(media_id):
            media_type = MediaType.MUSIC
            play_item = await media_source.async_resolve_media(self.hass, media_id, self.entity_id)
            # play_item returns a relative URL if it has to be resolved on the Home Assistant host
            # This call will turn it into a full URL
            media_id = async_process_play_media_url(self.hass, play_item.url)

        # Replace this with calling your media player play media function.
        await self._media_player.play_url(media_id)

    def play_media(self, media_type: MediaType | str, media_id: str, **kwargs: Any) -> None:
        service_data = {}
        service_data["entity_id"] = self._origin_entity
        service_data[ATTR_MEDIA_CONTENT_TYPE] = media_type
        service_data[ATTR_MEDIA_CONTENT_ID] = media_id
        service_data[ATTR_MEDIA_ENQUEUE] = kwargs[ATTR_MEDIA_ENQUEUE]
        service_data[ATTR_MEDIA_ANNOUNCE] = kwargs[ATTR_MEDIA_ANNOUNCE]
        self.hass.services.call(PLATFORM, 'play_media', service_data, False)

    def clear_playlist(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_CLEAR_PLAYLIST, {
                                        "entity_id": self._origin_entity}, False)

    def join_players(self, group_members: list[str]) -> None:
        self.hass.services.call(PLATFORM, SERVICE_JOIN, {
                                        "entity_id": self._origin_entity, ATTR_GROUP_MEMBERS : group_members}, False)
    def media_next_track(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_NEXT_TRACK, {
                                        "entity_id": self._origin_entity}, False)

    def media_pause(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_STOP, {
                                        "entity_id": self._origin_entity}, False)

    def media_play(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_PLAY, {
                                        "entity_id": self._origin_entity}, False)

    async def async_media_play_pause(self) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_MEDIA_PLAY_PAUSE, {
                                        "entity_id": self._origin_entity}, False)

    def media_previous_track(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_PREVIOUS_TRACK, {
                                        "entity_id": self._origin_entity}, False)

    def media_seek(self, position: float) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_SEEK, {
                                        "entity_id": self._origin_entity, ATTR_MEDIA_SEEK_POSITION : position}, False)

    def media_stop(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_MEDIA_STOP, {
                                        "entity_id": self._origin_entity}, False)
        
    def set_repeat(self, repeat: RepeatMode) -> None:
        self.hass.services.call(PLATFORM, SERVICE_REPEAT_SET, {
                                        "entity_id": self._origin_entity, "repeat" : repeat}, False)

    def select_sound_mode(self, sound_mode: str) -> None:
        self.hass.services.call(PLATFORM, SERVICE_SELECT_SOUND_MODE, {
                                        "entity_id": self._origin_entity, ATTR_SOUND_MODE: sound_mode}, False)

    def select_source(self, source: str) -> None:
        self.hass.services.call(PLATFORM, SERVICE_SELECT_SOURCE, {
                                        "entity_id": self._origin_entity, ATTR_INPUT_SOURCE: source}, False)

    def set_shuffle(self, shuffle: bool) -> None:
        self.hass.services.call(PLATFORM, SERVICE_SHUFFLE_SET, {
                                        "entity_id": self._origin_entity, ATTR_MEDIA_SHUFFLE: shuffle}, False)

    async def async_toggle(self) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_TOGGLE, {
                                        "entity_id": self._origin_entity}, False)

    def turn_on(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_TURN_ON, {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)
        
    def unjoin_player(self) -> None:
        self.hass.services.call(PLATFORM, SERVICE_UNJOIN, {
                                        "entity_id": self._origin_entity}, False)

    async def async_volume_down(self) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_VOLUME_DOWN, {
                                        "entity_id": self._origin_entity}, False)


    async def async_volume_up(self) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_VOLUME_UP, {
                                        "entity_id": self._origin_entity}, False)


    async def async_set_volume_level(self, volume: float) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_VOLUME_SET, {
                                        "entity_id": self._origin_entity, ATTR_MEDIA_VOLUME_LEVEL : volume}, False)


    async def async_mute_volume(self, mute: bool) -> None:
        await self.hass.services.async_call(PLATFORM, SERVICE_VOLUME_MUTE, {
                                        "entity_id": self._origin_entity, ATTR_MEDIA_VOLUME_MUTED : mute}, False)



    




