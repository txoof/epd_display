## Additional Plugin Information
### Configuration Notes
**Sample Configuration*
```
[Plugin: Moon Phases]
layout = layout
plugin = moon_phase
refresh_rate = 600
min_display_time = 40
max_priority = 2
location_name = America/Denver
# Failure to provide a unique identifier can result in a perma-ban from the Met.NO API
email = you@host.diamond
# Lat/Lon are optional, but will increase accuracy for moonrise and moonset times
lat = 39.739
lon = -104.985
```
**location_name**

To find the `location_name`, use `paperpi --run_plugin_func moon_phase.list_country_locales XX` where XX is the two letter [ISO 3116 country codes](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) to find the region/locale names.

**email**
The ***FREE*** APIs at MET.NO are available to everyone with no registration, no key and very few limitations. MET.NO offers this great API with the minor expectation that you identify yourself. Please fill in a real email address or risk being banned from the service.

**lat/lon**

To find the lat/lon of a particular location use `paperpi --run_plugin_func moon_phase.get_coord "City, Provence, Country"` The `lat` and `lon` values are entirely optional. If they are omitted the plugin will use the lat/lon of the `location_name`.

### Moon Images
The moon images are the first full lunar cycle of 2022: 2022.01.02 - 2022.02.01 and are sourced from [NASA](https://svs.gsfc.nasa.gov/4955). The images accurately show the relative size and angle of the moon relative to the earth for that month. 

### Moon Phase Data
The moon phase data is sourced from the [Norwegian Meteorolgisk Institutt](https://api.met.no/weatherapi/sunrise/2.0/documentation#!/data/get_format) API. MET provides tons of amazing free APIs with oceanic, meterological and air quality forecasts. Some of the information is limited to Norwegian locales, but other information such as the weather forecasts are available world-wide.