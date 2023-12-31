"""Config flow for Hello World integration."""
import logging
import voluptuous as vol
from typing import Any, Dict, Optional
from datetime import datetime

import homeassistant.helpers.config_validation as cv

import homeassistant.helpers.entity_registry

from homeassistant.helpers.device_registry import (
    async_get,
    async_entries_for_config_entry
)

from .const import *
from homeassistant.helpers import selector
from homeassistant import config_entries, exceptions
from homeassistant.core import callback

from homeassistant.helpers import (
    device_registry as dr,
    entity_platform,
    entity_registry as er,
)

import asyncio

_LOGGER = logging.getLogger(__name__)

OPTION_ADD_DEVICE = "add_entity"
OPTION_MODIFY_ENTITY = "modify_entity"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle the initial step."""
        errors = {}
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")
        """
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title=user_input[CONF_DEVICE_NAME], data=self.data)
        
        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_NAME, default=DOMAIN): cv.string
                }), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle a option flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow for the component."""
    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry
        self._selected_entity = None
        self._selected_conf = None
        self.data = {}
        if CONF_ENTITIES in config_entry.options:
            self.data[CONF_ENTITIES] = config_entry.options[CONF_ENTITIES]
        else:
            _LOGGER.debug("set entity dict")
            self.data[CONF_ENTITIES] = []

    async def remove_entity(self, entity_id, conf):
        self.data[CONF_ENTITIES].clear()
        # remove entity
        _LOGGER.debug("remove entity id : " + entity_id)
        entity = self._entity_registry.async_get(entity_id)
        _LOGGER.debug("entity info : " + str(entity))
        self._entity_registry.async_remove(entity_id)

        device_ids = set([])
        entities = er.async_entries_for_config_entry(self._entity_registry, self.config_entry.entry_id)
        device_registry = dr.async_get(self.hass)
        devices = dr.async_entries_for_config_entry(device_registry, self.config_entry.entry_id)

        for e in entities:
            device_ids.add(e.device_id)
            self.data[CONF_ENTITIES].append(self.hass.states.get(e.entity_id).attributes[ATTR_CONF])

        for d in devices:
            if d.id not in device_ids:
                device_registry.async_update_device(d.id, remove_config_entry_id=self.config_entry.entry_id)

    async def async_step_init(
        self, user_input: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        errors: Dict[str, str] = {}

        self._entity_registry = er.async_get(self.hass)

        dev_reg = dr.async_get(self.hass)

        if user_input is not None:
            if not errors:
                if user_input.get(CONF_OPTIONS_SELECT) == OPTION_ADD_DEVICE:
                    return await self.async_step_entity()
                elif user_input.get(CONF_OPTIONS_SELECT) == OPTION_MODIFY_ENTITY:
                    _LOGGER.debug("async step select")
                    return await self.async_step_select()
                else:
                    self.data["modifydatetime"] = datetime.now()
                    return self.async_create_entry(title=self.config_entry.data.get(CONF_DEVICE_NAME), data=self.data)
                
        option_devices = []
        option_devices.append(OPTION_ADD_DEVICE)
        option_devices.append(OPTION_MODIFY_ENTITY)
        
        options_schema = vol.Schema(
            {
                #vol.Optional(CONF_OPTIONS_SELECT): vol.In(option_devices),
                vol.Optional(CONF_OPTIONS_SELECT): selector.SelectSelector(selector.SelectSelectorConfig(options=option_devices, mode=selector.SelectSelectorMode.LIST, translation_key="option_select")),
                
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=options_schema, errors=errors
        )

    async def async_step_select(self, user_input: Optional[Dict[str, Any]] = None):
        """Second step in config flow to add a repo to watch."""
        self._selected_entity = None

        errors: Dict[str, str] = {}
        entities = er.async_entries_for_config_entry(
            self._entity_registry, self.config_entry.entry_id)

        if user_input is not None:
            if not errors:
                state = self.hass.states.get(user_input[CONF_SELECT_ENTITY])
                conf = state.attributes.get(ATTR_CONF)

                if user_input[CONF_REMOVE_ENTITY]:              
                    # remove config
                    _LOGGER.debug("conf : " + str(conf))
                    await self.remove_entity(user_input[CONF_SELECT_ENTITY], conf)
                    # create entry
                    self.data["modifydatetime"] = datetime.now()
                    return self.async_create_entry(title=self.config_entry.data.get(CONF_DEVICE_NAME), data=self.data)
                else:
                    # modify entity
                    self._selected_entity = user_input[CONF_SELECT_ENTITY]
                    self._selected_conf = conf
                    return await self.async_step_entity()

        include_entities = []
        for e in entities:
            include_entities.append(e.entity_id)

        return self.async_show_form(
            step_id="select",
            data_schema=vol.Schema(
                    {
                        vol.Required(CONF_SELECT_ENTITY, default=""): selector.EntitySelector(selector.EntitySelectorConfig(include_entities=include_entities)),
                        vol.Optional(CONF_REMOVE_ENTITY, default=False): cv.boolean,
                    }
            ), errors=errors
        )

    async def async_step_entity(self, user_input: Optional[Dict[str, Any]] = None):
        """Second step in config flow to add a repo to watch."""
        errors: Dict[str, str] = {}
        entity_registry = er.async_get(
            self.hass)
        dev_reg = dr.async_get(self.hass)

        if user_input is not None:
            if not errors:
                if self._selected_entity is not None and self._selected_conf is not None:
                    # remove entity
                    await self.remove_entity(self._selected_entity, self._selected_conf)

                # append entity
                self.data[CONF_ENTITIES].append(
                    [
                        user_input[CONF_ORIGIN_ENTITY],
                        user_input.get(CONF_DEST_DEVICE, None),
                        user_input[CONF_NAME],
                        user_input.get(CONF_PARENT_DEVICE_ENTITY_ID_FORMAT, False),
                        user_input.get(CONF_HIDE_ORIGIN_ENTITY, False),
                    ]
                )

                self.data["modifydatetime"] = datetime.now()
                return self.async_create_entry(title=self.config_entry.data.get(CONF_DEVICE_NAME), data=self.data)

        entity = []
        for key, value in ENTITY_TYPE.items():
            for e in value:
                entity.append(e)

        _LOGGER.debug("selected conf is : " + str(self._selected_conf))
        return self.async_show_form(
            step_id="entity",
            data_schema=vol.Schema(
                    {
                        vol.Required(CONF_ORIGIN_ENTITY, default=self._selected_conf[0] if self._selected_conf is not None else None): selector.EntitySelector(selector.EntitySelectorConfig(domain=entity)),
                        vol.Optional(CONF_DEST_DEVICE, description={"suggested_value": self._selected_conf[1] if self._selected_conf is not None else None}): selector.DeviceSelector(selector.DeviceSelectorConfig()),
                        vol.Required(CONF_NAME, default=self._selected_conf[2] if self._selected_conf is not None else None): cv.string,
                        vol.Optional(CONF_PARENT_DEVICE_ENTITY_ID_FORMAT, description={"suggested_value": self._selected_conf[3] if self._selected_conf is not None and len(self._selected_conf) >= 4 else False}): selector.BooleanSelector(selector.BooleanSelectorConfig()),
                        vol.Optional(CONF_HIDE_ORIGIN_ENTITY, description={"suggested_value": self._selected_conf[4] if self._selected_conf is not None and len(self._selected_conf) >= 5 else False}): selector.BooleanSelector(selector.BooleanSelectorConfig())
                    }
            ), errors=errors
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
