"""Sensor platform exposing a weather entity's attributes as sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import ATTRIBUTES, CONF_SOURCE, DOMAIN, WeatherAttribute

_UNAVAILABLE = ("unavailable", "unknown")


def _resolve_unit(desc: WeatherAttribute, state: State | None) -> str | None:
    """Resolve a sensor's unit: a fixed one, else the entity's *_unit attribute."""
    if desc.fixed_unit is not None:
        return desc.fixed_unit
    if state is not None and desc.unit_attribute is not None:
        return state.attributes.get(desc.unit_attribute)
    return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create a sensor for each attribute the source weather entity exposes."""
    source: str = entry.data[CONF_SOURCE]
    state = hass.states.get(source)
    # If the source is already loaded, only create sensors for attributes it has;
    # otherwise create all known ones (they stay unavailable until it appears).
    present = set(state.attributes) if state is not None else None

    async_add_entities(
        WeatherAttributeSensor(entry, desc, _resolve_unit(desc, state))
        for desc in ATTRIBUTES
        if present is None or desc.attribute in present
    )


class WeatherAttributeSensor(SensorEntity):
    """A single weather attribute mirrored as a sensor."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self, entry: ConfigEntry, desc: WeatherAttribute, unit: str | None
    ) -> None:
        self._source: str = entry.data[CONF_SOURCE]
        self._desc = desc
        self._attribute = desc.attribute
        self._attr_translation_key = desc.translation_key
        self._attr_unique_id = f"{entry.entry_id}_{desc.attribute}"
        self._attr_device_class = desc.device_class
        self._attr_state_class = desc.state_class
        self._attr_native_unit_of_measurement = unit
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data.get(CONF_NAME) or self._source,
            manufacturer="Weather to Sensors",
        )

    @property
    def native_value(self) -> float | int | None:
        """Return the attribute's current value from the source entity."""
        state = self.hass.states.get(self._source)
        if state is None:
            return None
        return state.attributes.get(self._attribute)

    @property
    def available(self) -> bool:
        """Available when the source is up and still exposes the attribute."""
        state = self.hass.states.get(self._source)
        return (
            state is not None
            and state.state not in _UNAVAILABLE
            and state.attributes.get(self._attribute) is not None
        )

    async def async_added_to_hass(self) -> None:
        """Update whenever the source weather entity changes."""
        # Re-resolve the unit now: at platform setup the source may not have
        # been loaded yet (e.g. the weather integration loads after this one),
        # which would otherwise leave the sensor permanently unit-less.
        self._update_unit()
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._source], self._source_changed
            )
        )

    @callback
    def _update_unit(self) -> None:
        """Refresh the unit from the source, keeping the last known one.

        The unit is read from the source's ``*_unit`` attribute, which only
        appears once the weather entity is loaded. We never overwrite a known
        unit with ``None`` so the sensor doesn't flap to unit-less (which would
        invalidate long-term statistics) while the source is briefly missing.
        """
        unit = _resolve_unit(self._desc, self.hass.states.get(self._source))
        if unit is not None:
            self._attr_native_unit_of_measurement = unit

    @callback
    def _source_changed(self, event) -> None:
        self._update_unit()
        self.async_write_ha_state()
