import logging

from .const import *
import re
from homeassistant.components.camera import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "camera"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, Camera):

    # platform property #############################################################################
    @property
    def is_recording(self) -> bool:
        return self._state == STATE_RECORDING

    @property
    def is_streaming(self) -> bool:
        return self._state == STATE_STREAMING

    @property
    def motion_detection_enabled(self) -> bool:
        return self._attributes.get("motion_detect_enabled")
    
    @property
    def is_on(self) -> bool:
        return self._attributes.get("is_on")

    @property
    def brand(self) -> str | None:
        return self._attributes.get("brand")

    @property
    def model(self) -> str | None:
        return self._attributes.get("model")

    @property
    def frame_interval(self) -> float:
        return self._attributes.get("frame_interval")

    @property
    def frontend_stream_type(self) -> StreamType | None:
        return self._attributes.get("frontend_stream_type")

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else CameraEntityFeature.ON_OFF | CameraEntityFeature.STREAM
    

    # method ########################################################################################
    def camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        raise NotImplementedError()

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""

    async def stream_source(self) -> str | None:
        return await super().stream_source()

    async def async_turn_on(self) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    def turn_on(self) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    async def async_turn_off(self) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_TURN_OFF, {
                                        "entity_id": self._origin_entity}, False)

    async def async_enable_motion_detection(self) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_ENABLE_MOTION, {
                                        "entity_id": self._origin_entity}, False)

    def enable_motion_detection(self) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_ENABLE_MOTION, {
                                        "entity_id": self._origin_entity}, False)

    async def async_disable_motion_detection(self) -> None:
        return await self.hass.services.async_call(PLATFORM, SERVICE_DISABLE_MOTION, {
                                        "entity_id": self._origin_entity}, False)

    def disable_motion_detection(self) -> None:
        return self.hass.services.call(PLATFORM, SERVICE_DISABLE_MOTION, {
                                        "entity_id": self._origin_entity}, False)
