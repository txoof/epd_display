# mod_name
![sample image for plugin met_no](../documentation/images/met_no_sample.png)
```

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
 
```