DOMAIN = "entity_copy"
NAME = "Entity Copy"
VERSION = "1.0.0"

#ENTITY_ID_FORMAT = DOMAIN + ".{}"
CONF_ORIGIN_ENTITY = "origin_entity"
CONF_ENTITIES = "entities"
CONF_SELECT_ENTITY = "select_entity"
CONF_REMOVE_ENTITY = "remove_entity"
CONF_OPTIONS_SELECT = "options_select"
CONF_DEST_DEVICE = "dest_device"
CONF_NAME = "name"

ATTR_CONF = "configure"

ENTITY_TYPE = {
    "sensor" : { "sensor", },
    "binary_sensor" : { "binary_sensor", },
    "switch" : { "switch", "input_boolean" },
    "number" : { "number", "input_number" },
    "button" : { "button" },
    "fan" : { "fan" },
    "cover": { "cover" },
    "climate": { "climate" },
    "select": { "select", "input_select" },
    "light": { "light" },
    "text": { "text", "input_text" },
    "lock": { "lock" },
    "camera": { "camera" },
    "media_player": { "media_player" },
    "weather": { "weather" },
    "remote": { "remote" },
    "device_tracker": { "device_tracker" },
    "siren": { "siren" },
    "humidifier": { "humidifier" },
}
