import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = "0.1.0"
name = "PaperPi Met No Weather plugin"

# open street maps location lookup
osm_endpoint = 'https://nominatim.openstreetmap.org/search/'
osm_query = "?format=json&addressdetails=0&limit=0"

# met.no endpoints
yr_endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/complete.json?"

# local images
symbol_codes_path = dir_path+"/./images/symbol_codes/"
wind_barbs_path = dir_path+"/./images/wind_barbs/"

abreviations = {'celsius': '°C',
                'fahrenheit': '°F',
                'degrees': '',
                'kelvin': 'K',
                '1': ' of 1',
                'inch': ' in',
                'knot': ' kt',
                'm/h': ' m/h',
                'm/s': ' m/s',
                'mm': ' mm',
                }

text = {'t_precipitation': 'Precipitation',
        't_max': 'Max',
        't_min': 'Min',
        't_temperature': 'Temperature',
        't_wind': 'Wind',
        't_presure': 'Presure',
        't_humidity': 'Humidity',
        't_wind_direction': 'Wind Direction',
        't_uv_index': 'UV Index',
        }

