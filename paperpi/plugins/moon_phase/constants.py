# relative paths are difficult to sort out -- this makes it easier
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.2.0'
name = 'moon_phase'
data = {
    'moonrise': 'time moon appears above horizon',
    'moonset': 'time moon sets below horizon',
    'age': 'days since new (no) moon',
    'image_file': 'location of image file to display',
    'phase_desc': 'description of phase e.g. Waxing Crescent'

}

# open street maps location lookup
osm_endpoint = 'https://nominatim.openstreetmap.org/search/'
osm_query = "?format=json&addressdetails=0&limit=0"

# met.no endpoints
met_endpoint = "https://api.met.no/weatherapi/sunrise/2.0/.json?"

# configuration keys required for opperation
required_config_options = {
    'lat': None,  
    'lon': None, 
    'location_name': 'Europe/Amsterdam',
    'email': None,
}


json_file = f'{name}.json'
# set to 6 hrs * 60 min * 60 seconds 
json_max_age = 60*60*6

#API JSON dictionary locations
addr_phase = 'location.time.0.moonphase'
addr_rise = 'location.time.0.moonrise'
addr_set = 'location.time.0.moonset'

# image file constants
image_path = dir_path+"/./images/"
img_suffix = '.jpeg'

# data template
data_template = {
    'moonrise': 'Moonrise: {}',
    'moonset': 'Moonset: {}',
    'phase_desc': 'Phase: {}',
    'age': 'Age: {} days',
    'image_file': '{}',
    'phase_desc': '{}'
    
}

sample_config = '''
[Plugin: Moon Phase]
# default layout
layout = layout
plugin = moon_phase
min_display_time = 30
max_priority = 2
# your email address for MET.no API access -- failure to specify may lead to a perma-ban
email = you@host.diamond
# Timezone locale name in Region/City format (see --run_plugin_func moon_phase.list_country_locales)
# Use a known city in your timezone; this is critical for calculating the moonrise time
location_name = Europe/Amsterdam
# lat/lon of your physical location (optional) (see --run_plugin_func moon_phase.get_coord)
lat = 52.3
lon = 4.9
'''
