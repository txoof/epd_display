# met_no
![sample image for plugin met_no](met_no_sample.png)
```

PLUGIN: met_no v:0.1.0


FUNCTION: get_coord
USER FACING HELPER FUNCTION:
    lookup and print the latitude, longitude of a place given as a string:
    
    usage: --run_plugin_func met_no.get_coord "Horsetooth Reservoir, Fort Collins CO, USA"
    
    Args:
        place(`str`): "City, Provence, Country
    
    Returns:
        `tuple`: lat, lon
        
    Example:
        get_coord("Denver, Colorado, USA")
        get_coord("Bamako, Mali")
        
___________________________________________________________________________
 
FUNCTION: update_function
update function for met_no plugin provides extensive forecast data
    
    This plugin provides hourly forecast data for a given location. 
    Data is pulled from the Norwegian Meterological Institute (met.no)
    Multiple met_no plugins can be active each with different locations 
    
    Forecast images are provided courtesy of Met.no
    
    All "local" time strings are converted to the system time
    
    Configuration Requirements:
        self.config(`dict`): {
            'lat': latitude of forecast location (`float`),
            'lon': longitude of forecast location (`float`),
            'location_name': name of location (`str`)
            'email': user contact email address -- required by met.no (`str`)
            'temp_units': 'celsius' or 'fahrenheit' (`str`), #optional
            'rain_units': 'mm' or 'inch' (`str`), #optional
            'windspeed': 'm/s', 'm/h', 'knot', 'k/h' (`str)#optional
        }
        self.cache(`CacheFiles` object)
        
    Args:
        self(namespace): namespace from plugin object
    
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))
    
___________________________________________________________________________
 


SAMPLE CONFIGURATION FOR plugins.met_no.met_no

[Plugin: Weather Adis Ababa]
layout = layout
plugin = met_no
refresh_rate = 300
min_display_time = 40
location_name = Adis Ababa
lat = 9.000
lon = 38.750
# this is required by Met.no -- please use a real value
email = you@host.diamond


LAYOUTS AVAILABLE:
  layout
  test
  three_column_icon_wind_temp_precip
  two_column_icon_wind_temp_precip


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.met_no.met_no:
   no keys available
```