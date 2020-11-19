# met_no
![sample image for plugin met_no](../documentation/images/met_no_sample.png)
```

PLUGIN: met_no v:0.1.0


FUNCTION: get_coord
lookup the lat, lon of a place given as a string:
    
    Args:
        place(`str`): "City, Provence, Country
    
    Returns:
        `tuple`: lat, lon
    Example:
        get_coord("Denver, Colorado, USA")
        get_coord("Bamako, Mali")
        
___________________________________________________________________________
 
FUNCTION: update_function
update_function for met_no Plugin() object to fetch forecast data for a lat, lon
    
    multiple met_no plugins can be active each with different locations 
    
    all "local" time strings are converted to the system time
    
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
    
    
___________________________________________________________________________
 

LAYOUTS AVAILABLE:
  layout
  test
  three_column_icon_wind_temp_precip
  two_column_icon_wind_temp_precip


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.met_no.met_no:
   no keys available
```