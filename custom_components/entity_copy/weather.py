import logging

from .const import *
import re
from homeassistant.components.weather import (
    WeatherEntity,
    ATTR_WEATHER_CLOUD_COVERAGE,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_APPARENT_TEMPERATURE,
    ATTR_WEATHER_DEW_POINT,
    ATTR_WEATHER_PRECIPITATION_UNIT,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_PRESSURE_UNIT,
    ATTR_WEATHER_VISIBILITY,
    ATTR_WEATHER_VISIBILITY_UNIT,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_PRESSURE_UNIT,
    ATTR_WEATHER_VISIBILITY,
    ATTR_WEATHER_VISIBILITY_UNIT,
    ATTR_WEATHER_WIND_GUST_SPEED,
    ATTR_WEATHER_WIND_SPEED,
    ATTR_WEATHER_WIND_SPEED_UNIT,
    ATTR_WEATHER_OZONE,
    ATTR_WEATHER_WIND_BEARING,
)

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "weather"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, WeatherEntity):

    # platform property ##############################################################################
    # @property
    # def forecast(self) -> list[Forecast] | None:
    #     return self._attributes.get(ATTR_FORECAST)

    @property
    def cloud_coverage(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_CLOUD_COVERAGE)

    @property
    def condition(self) -> str | None:
        return self._attributes.get("condition")

    @property
    def humidity(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_HUMIDITY)

    @property
    def native_apparent_temperature(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_APPARENT_TEMPERATURE)

    @property
    def native_dew_point(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_DEW_POINT)

    @property
    def native_precipitation_unit(self) -> str | None:
        return self._attributes.get(ATTR_WEATHER_PRECIPITATION_UNIT)

    @property
    def native_pressure(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_PRESSURE)

    @property
    def native_pressure_unit(self) -> str | None:
        return self._attributes.get(ATTR_WEATHER_PRESSURE_UNIT)

    @property
    def native_visibility(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_VISIBILITY)

    @property
    def native_visibility_unit(self) -> str | None:
        return self._attributes.get(ATTR_WEATHER_VISIBILITY_UNIT)

    @property
    def native_wind_gust_speed(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_WIND_GUST_SPEED)

    @property
    def native_wind_speed(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_WIND_SPEED)

    @property
    def native_wind_speed_unit(self) -> str | None:
        return self._attributes.get(ATTR_WEATHER_WIND_SPEED_UNIT)

    @property
    def ozone(self) -> float | None:
        return self._attributes.get(ATTR_WEATHER_OZONE)

    @property
    def uv_index(self) -> float | None:
        return self._attributes.get("uv_index")

    @property
    def wind_bearing(self) -> float | str | None:
        return self._attributes.get(ATTR_WEATHER_WIND_BEARING)

    # @property
    # def supported_features(self) -> int | None:
    #     return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else WeatherEntityFeature.FORECAST_DAILY

    # method #########################################################################################


