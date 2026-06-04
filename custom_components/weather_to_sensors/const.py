"""Constants and the attribute → sensor mapping for Weather to Sensors."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import DEGREE, PERCENTAGE

DOMAIN = "weather_to_sensors"

# Config key: the source weather.* entity whose attributes we expose.
CONF_SOURCE = "source"


@dataclass(frozen=True, kw_only=True)
class WeatherAttribute:
    """Describes how one weather attribute becomes a sensor."""

    attribute: str
    translation_key: str
    device_class: SensorDeviceClass | None = None
    # Attribute on the weather entity that holds the unit (e.g. temperature_unit).
    unit_attribute: str | None = None
    # Unit to use when the entity does not provide one (e.g. % for humidity).
    fixed_unit: str | None = None
    state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT


# Standard weather entity attributes (see Home Assistant's weather integration).
# A sensor is only created for the attributes a given entity actually exposes.
ATTRIBUTES: tuple[WeatherAttribute, ...] = (
    WeatherAttribute(
        attribute="temperature",
        translation_key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        unit_attribute="temperature_unit",
    ),
    WeatherAttribute(
        attribute="apparent_temperature",
        translation_key="apparent_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        unit_attribute="temperature_unit",
    ),
    WeatherAttribute(
        attribute="dew_point",
        translation_key="dew_point",
        device_class=SensorDeviceClass.TEMPERATURE,
        unit_attribute="temperature_unit",
    ),
    WeatherAttribute(
        attribute="humidity",
        translation_key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        fixed_unit=PERCENTAGE,
    ),
    WeatherAttribute(
        attribute="pressure",
        translation_key="pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        unit_attribute="pressure_unit",
    ),
    WeatherAttribute(
        attribute="wind_speed",
        translation_key="wind_speed",
        device_class=SensorDeviceClass.WIND_SPEED,
        unit_attribute="wind_speed_unit",
    ),
    WeatherAttribute(
        attribute="wind_gust_speed",
        translation_key="wind_gust_speed",
        device_class=SensorDeviceClass.WIND_SPEED,
        unit_attribute="wind_speed_unit",
    ),
    # Wind bearing has no device class; no state_class to avoid averaging a
    # circular value across the 0/360 wrap.
    WeatherAttribute(
        attribute="wind_bearing",
        translation_key="wind_bearing",
        fixed_unit=DEGREE,
        state_class=None,
    ),
    WeatherAttribute(
        attribute="cloud_coverage",
        translation_key="cloud_coverage",
        fixed_unit=PERCENTAGE,
    ),
    WeatherAttribute(
        attribute="uv_index",
        translation_key="uv_index",
    ),
    WeatherAttribute(
        attribute="visibility",
        translation_key="visibility",
        device_class=SensorDeviceClass.DISTANCE,
        unit_attribute="visibility_unit",
    ),
    WeatherAttribute(
        attribute="ozone",
        translation_key="ozone",
    ),
)
