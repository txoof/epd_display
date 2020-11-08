version = "0.1.0"
name = "YR Weather"

osm_endpoint = 'https://nominatim.openstreetmap.org/search/'
osm_query = "?format=json&addressdetails=0&limit=0"

yr_endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/complete.json?"

symbol_codes_path = "./images/symbol_codes/"
wind_barbs_path = "./images/wind_barbs/"

abreviations = {'celsius': 'C',
                'fahrenheit': 'F',
                'degrees': '',
                '1': ' of 1',
                'inch': ' in',
                'knot': ' kt',
                'm/h': ' m/h',
                'm/s': ' m/s',
                'mm': ' mm',
                }

