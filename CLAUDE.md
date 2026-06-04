# Weather to Sensors — project notes (for a fresh session)

A small Home Assistant **custom integration** that exposes a `weather.*` entity's
attributes (temperature, humidity, pressure, wind, …) as regular **sensors**
with the correct `unit_of_measurement` (read from the entity's `*_unit`
attributes) and `device_class`.

It was extracted from work on `home-assistant-weewx-scrape`: the WeeWX dashboard
strategy could overlay other weather sources, but values read from a `weather.*`
**attribute** (e.g. Met.no) showed up without units, because attributes carry no
`unit_of_measurement`. Rather than bake source-specific logic into that
integration, this generic helper turns any weather entity's attributes into
proper sensors that every card/history handles natively.

## Status

- Functionally complete first cut (v0.1.0), not yet published or tested in a
  live Home Assistant.
- UI config flow (pick a `weather.*` entity + optional name), one device per
  source, a sensor per exposed attribute, updates via state-change tracking.

## Layout

```
custom_components/weather_to_sensors/
  __init__.py        # entry setup/unload, forwards to the sensor platform
  manifest.json      # domain weather_to_sensors, integration_type "helper"
  config_flow.py     # EntitySelector(domain="weather") + optional name
  const.py           # DOMAIN, CONF_SOURCE, ATTRIBUTES mapping table
  sensor.py          # WeatherAttributeSensor: reads attr + *_unit from source
  strings.json, translations/{en,de}.json
.github/workflows/
  validate.yml       # hassfest + HACS validation
  release.yml        # builds weather_to_sensors.zip (release + workflow_dispatch)
hacs.json            # zip_release integration
README.md, LICENSE
```

## How it works

`const.ATTRIBUTES` lists the standard weather attributes with their device class
and where to get the unit (`unit_attribute` like `temperature_unit`, or a
`fixed_unit` like `%`/`°`). `sensor.py` creates a sensor per attribute the source
exposes; `native_value` reads `state_attr(source, attribute)`, the unit is
resolved once at setup, and each sensor re-renders on the source's state changes.

## Next steps / TODO

1. **Create the GitHub repo** `home-assistant-weather-to-sensors` (public) and
   push these files. (Update the `documentation`/`issue_tracker` URLs in
   `manifest.json` if you pick a different name.)
2. Cut a pre-release: Actions → run the **release** workflow (`workflow_dispatch`)
   with tag `v0.1.0`, prerelease = true. It builds and attaches the zip.
3. Add the repo to HACS as a custom **Integration**, install, restart HA.
4. Test: add the integration, pick `weather.forecast_home`, confirm sensors get
   units (°C/hPa/%/km/h/°) and values track the weather entity.
5. Point the WeeWX dashboard's Met.no source at the new `sensor.*` entities
   (instead of `weather.forecast_home[attribute]`), so units show in the header.

## Ideas / possible follow-ups

- Options flow to choose which attributes to expose.
- Skip creating sensors for attributes that are permanently `None`.
- `apparent_temperature`/`dew_point`/`ozone` etc. only exist on some providers —
  already handled (only present attributes become sensors), but worth a test
  across Met.no, MeteoSwiss, OpenWeatherMap.
- Consider `integration_type: "helper"` vs `"service"` and whether to attach the
  sensors to the source device instead of a new device.
