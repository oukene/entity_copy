import asyncio
from .const import *
from homeassistant.helpers.entity import Entity

import logging
import re
from homeassistant.const import (
    STATE_UNKNOWN, STATE_UNAVAILABLE,
)
from threading import Timer

from .const import *
from homeassistant.helpers.entity import DeviceInfo, async_generate_entity_id
from homeassistant.helpers.event import async_track_state_change

import homeassistant

from homeassistant.helpers import (
    device_registry as dr,
    entity_platform,
    entity_registry as er,
)

from homeassistant.helpers.entity_registry import RegistryEntryHider

from homeassistant.helpers import config_validation as cv, discovery, entity, service

from homeassistant.const import (
    ATTR_ASSUMED_STATE, ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT, ATTR_ENTITY_PICTURE
)

ENTITY_ID_FORMAT = DOMAIN + ".{}"

_LOGGER = logging.getLogger(__name__)

def _is_valid_state(state) -> bool:
    return state and state.state != STATE_UNKNOWN and state.state != STATE_UNAVAILABLE

async def async_setup(hass, platform, entity_type, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN][config_entry.entry_id]["listener"] = []
    
    # _LOGGER.debug("data : %s", config_entry.data)
    # _LOGGER.debug("options : %s", config_entry.options)
    device = hass.data[DOMAIN][config_entry.entry_id]["device"]

    new_devices = []

    if config_entry.options.get(CONF_ENTITIES) != None:
        for conf in config_entry.options.get(CONF_ENTITIES):
            #_LOGGER.debug("key : %s", key)
            #entity = config_entry.options[CONF_ENTITIES][key]
            for e in ENTITY_TYPE[platform]:
                if re.search("^" + e, conf[0]):
                    #_LOGGER.debug("PLATFORM : %s, add entity : %s, entity : %s", platform, entity, entity)
                    new_devices.append(
                        entity_type(
                            hass,
                            config_entry.entry_id,
                            device,
                            conf,
                        )
                    )
                    continue

        if new_devices:
            async_add_devices(new_devices)

class Device:
    def __init__(self, name, config):
        self._id = f"{name}_{config.entry_id}"
        self._name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self.firmware_version = VERSION
        self.model = "astar"
        self.manufacturer = "astar"

    @property
    def device_id(self):
        """Return ID for roller."""
        return self._id

    @property
    def name(self):
        return self._name

    def register_callback(self, callback):
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback):
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()



class EntityBase(Entity):

    should_poll = False

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._device.remove_callback(self.async_write_ha_state)


    def __init__(self, hass, entry_id, device, conf):
        """Initialize the sensor."""
        super().__init__()
        self._device = device
        self.hass = hass
        self._name = conf[2]
        self._dest_device_id = conf[1]
        self._origin_entity = conf[0]
        self._entry_id = entry_id
        self._conf = conf

        self._device_info = DeviceInfo(identifiers={(DOMAIN, self._device.device_id)},
                                       name=self._device.name,
                                       sw_version=self._device.firmware_version,
                                       model=self._device.model,
                                       manufacturer=self._device.manufacturer
                                       )

        dev_reg = dr.async_get(hass)
        # Resolve source entity device
        if (
            (self._dest_device_id is not None)
            and (
                (
                    device := dev_reg.async_get(
                        device_id=self._dest_device_id,
                    )
                )
                is not None
            )
        ):
            self._device_info = DeviceInfo(
                identifiers=device.identifiers,
                name=device.name,
                sw_version=device.sw_version,
                model=device.model,
                manufacturer=device.manufacturer
            )

        device_name = self._device_info["name"] if len(conf) >= 4 and conf[3] else self._device.name
        """
        device_registry = dr.async_get(hass)
        devices = dr.async_entries_for_config_entry(
            device_registry, entry.entry_id)
        device_name = entry.data.get(CONF_DEVICE_NAME)
        for d in devices:
            if entry.entry_id in (d.config_entries):
                device_name = d.name_by_user if d.name_by_user else d.name
        """

        if len(conf) >= 5 and conf[4]:
            er.async_get(hass).async_update_entity(entity_id=self._origin_entity, hidden_by=RegistryEntryHider.USER)
        else:
            try:
                er.async_get(hass).async_update_entity(entity_id=self._origin_entity, hidden_by=None)
            except Exception as e:
                """"""

        self._unique_id = async_generate_entity_id(ENTITY_ID_FORMAT, "{}_{}".format(device_name, self._name), current_ids="", hass=hass)
        self.entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, "{}_{}".format(device_name, self._name), current_ids="", hass=hass)

        registry = er.async_get(hass)
        origin_entity = registry.async_get(self._origin_entity)

        _LOGGER.debug("entity_id : %s", self.entity_id)

        self._state = None
        self._attributes = {}
        
        self.hass.data[DOMAIN][self._entry_id]["listener"].append(async_track_state_change(
            self.hass, self._origin_entity, self.entity_listener))
        new_state = self.hass.states.get(self._origin_entity)
        old_state = self.hass.states.get(self.entity_id)
        _LOGGER.debug("origin entity state - " + str(new_state))

        self.entity_listener(self._origin_entity, old_state, new_state)


    def entity_listener(self, entity, old_state, new_state):
        _LOGGER.debug("call entity listener2")
        if _is_valid_state(new_state):
            self._attributes = new_state.attributes.copy()
            _LOGGER.debug("attributes : " + str(self._attributes))
            self._attributes[ATTR_CONF] = self._conf
            #self._attributes[CONF_ORIGIN_ENTITY] = self._origin_entity_id
            self._state = new_state.state
            _LOGGER.debug("new_state.state : " + str(new_state.state))
            self.schedule_update_ha_state()
            #self._device.publish_updates()

    # default property ###############################################################################################
    @property
    def device_info(self) -> DeviceInfo | None:
        return self._device_info

    @property
    def has_entity_name(self) -> bool:
        return True

    @property
    def assumed_state(self) -> bool:
        return self._attributes[ATTR_ASSUMED_STATE] if self._attributes.get(ATTR_ASSUMED_STATE) != None else None

    @property
    def device_class(self):
        return self._attributes[ATTR_DEVICE_CLASS] if self._attributes.get(ATTR_DEVICE_CLASS) != None else None

    @property
    def native_unit_of_measurement(self):
        """Return the unit_of_measurement of the device."""
        return self._attributes[ATTR_UNIT_OF_MEASUREMENT] if self._attributes.get(ATTR_UNIT_OF_MEASUREMENT) != None else None

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attributes

    @property
    def entity_picture(self) -> str | None:
        return self._attributes[ATTR_ENTITY_PICTURE] if self._attributes.get(ATTR_ENTITY_PICTURE) != None else None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self) -> str | None:
        return super().icon

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        if self._unique_id is not None:
            return self._unique_id

    @property
    def state(self):
        return self._state