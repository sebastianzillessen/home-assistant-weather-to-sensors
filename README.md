# Weather to Sensors — Home Assistant integration

Turn a **`weather.*` entity's attributes into regular sensors.**

Home Assistant's `weather` entities keep their readings (temperature, humidity,
pressure, wind speed/bearing, …) as **attributes**, which carry no
`unit_of_measurement`. That makes them awkward for charts and history: cards such
as [apexcharts-card](https://github.com/RomRider/apexcharts-card) show the value
without a unit, and you can't pick the attribute as a normal sensor.

This helper creates one sensor per attribute, with the **correct unit** (read
from the entity's own `*_unit` attributes, e.g. `temperature_unit`) and a proper
**device class** — so they behave like any other sensor.

## What it creates

For a chosen weather entity, a sensor is created for each of these attributes it
exposes:

| Sensor | Device class | Unit |
| --- | --- | --- |
| Temperature | temperature | from `temperature_unit` |
| Apparent temperature | temperature | from `temperature_unit` |
| Dew point | temperature | from `temperature_unit` |
| Humidity | humidity | % |
| Pressure | atmospheric pressure | from `pressure_unit` |
| Wind speed | wind speed | from `wind_speed_unit` |
| Wind gust speed | wind speed | from `wind_speed_unit` |
| Wind bearing | – | ° |
| Cloud coverage | – | % |
| UV index | – | – |
| Visibility | distance | from `visibility_unit` |
| Ozone | – | – |

Only attributes the entity actually exposes become sensors. All sensors live
under one device named after the source entity, and update whenever it does.

## Installation (HACS)

1. HACS → three-dot menu → **Custom repositories** → add
   `https://github.com/sebastianzillessen/home-assistant-weather-to-sensors`
   with category **Integration**.
2. Install **Weather to Sensors** and restart Home Assistant.

## Configuration

UI only — no YAML.

1. **Settings → Devices & Services → Add Integration → Weather to Sensors.**
2. Pick the **weather entity** (e.g. `weather.forecast_home`) and, optionally, a
   name.
3. Done — the sensors appear under a new device.

Add the integration again to expose another weather entity.

## Why a separate integration?

It's deliberately generic: it works with **any** weather provider (Met.no,
MeteoSwiss, OpenWeatherMap, …), not one specific source, so it has no business
living inside a source-specific integration. The Home Assistant–native
alternative is a **Template** helper per attribute; this just automates that for
a whole weather entity with the right units and device classes.

## License

[MIT](LICENSE)
