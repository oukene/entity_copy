import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, ENTITY_TYPE

from .device import Device


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Hello World component."""
    # Ensure our name space for storing objects is a known type. A dict is
    # common/preferred as it allows a separate instance of your class for each
    # instance that has been created in the UI.
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    # Store an instance of the "connecting" class that does the work of speaking
    # with your actual devices.
    _LOGGER.debug("call async_setup_entry entry : " + str(entry))
    #hass.data[DOMAIN][entry.entry_id] = DOMAIN
    hass.data[DOMAIN][entry.entry_id] = {}
    hass.data[DOMAIN][entry.entry_id]["listener"] = []

    hass.data[DOMAIN][entry.entry_id]["device"] = Device(DOMAIN, entry)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    #entry.add_update_listener(update_listener)
    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    for component in ENTITY_TYPE.keys():
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )


    return True


async def update_listener(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("call async_unload_entry : " + entry.entry_id)

    for listener in hass.data[DOMAIN][entry.entry_id]["listener"]:
        listener()

    try:
        unload_ok = all(
            await asyncio.gather(
                *[
                    hass.config_entries.async_forward_entry_unload(
                        entry, component)
                    for component in ENTITY_TYPE.keys()
                ]
            )
        )

    except Exception as e:
        _LOGGER.error("except error : " + str(e))

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.debug("call async_unload_entry end")
    return unload_ok
