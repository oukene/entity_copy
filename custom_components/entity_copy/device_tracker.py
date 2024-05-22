import logging

from .const import *
import re
from homeassistant.components.device_tracker import TrackerEntity, ScannerEntity, ATTR_LOCATION_NAME
from homeassistant.components.device_tracker.config_entry import *

from .device import EntityBase, async_setup

_LOGGER = logging.getLogger(__name__)

PLATFORM = "device_tracker"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, TrackerEntity, ScannerEntity):

    # platform property ##############################################################################
    @property
    def source_type(self) -> SourceType | str:
        return self._attributes.get(ATTR_SOURCE_TYPE)

    @property
    def is_connected(self) -> bool:
        return self._state == STATE_HOME

    @property
    def battery_level(self) -> int | None:
        return self._attributes.get(ATTR_BATTERY_LEVEL)

    @property
    def ip_address(self) -> str | None:
        return self._attributes.get(ATTR_IP)

    @property
    def mac_address(self) -> str | None:
        return self._attributes.get(ATTR_MAC)

    @property
    def hostname(self) -> str | None:
        return self._attributes.get(ATTR_HOST_NAME)

    @property
    def latitude(self) -> float | None:
        return self._attributes.get(ATTR_LATITUDE)

    @property
    def longitude(self) -> float | None:
        return self._attributes.get(ATTR_LONGITUDE)

    @property
    def location_accuracy(self) -> int:
        return self._attributes.get(ATTR_GPS_ACCURACY)
    
    @property
    def location_name(self) -> str | None:
        return self._attributes.get(ATTR_LOCATION_NAME)
        
    # method #########################################################################################


