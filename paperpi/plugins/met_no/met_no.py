#!/usr/bin/env python3
# coding: utf-8




from copy import deepcopy
import requests
import logging
from urllib.parse import quote
import constants
from dictor import dictor
from pathlib import Path
from PIL import Image
import dateutil
import datetime








logger = logging.getLogger(__name__)






def get_coord(place=None):
    '''lookup the lat, lon of a place given as a string:
    
    Args:
        place(`str`): "City, Provence, Country
    
    Returns:
        `tuple`: lat, lon
    Example:
        get_coord("Denver, Colorado, USA")
        get_coord("Bamako, Mali")
        '''
    lat, lon = None, None
    if not place:
        print('lookup the lat/lon of city, town or geographic area')
        print('usage: paperpi -m met_no.get_coord "City, Area, Country"')
        print('paperpi -m met_no.get_coord "Golden Colorado, USA"')
        return (lat, lon)
    osm_endpoint = constants.osm_endpoint
    osm_query = constants.osm_query
    place_quote = quote(place)
    url = f'{osm_endpoint}{place_quote}{osm_query}'
    try:
        result = requests.get(url)
    except requests.RequestException as e:
        logging.warning(f'could not process request: {e}')
    if result.status_code == 200:
        if len(result.json()) > 0:
            lat = dictor(result.json()[0], 'lat')
            lon = dictor(result.json()[0], 'lon')
            display_name = dictor(result.json()[0], 'display_name')
            print(f'{display_name}\n{place}: {float(lat):.3f}, {float(lon):.3f}')
        else:
            print(f'no data was returned for place: {place}')
            print(f'check the spelling or try a more general query')
    else:
        print(f'No valid data was returned: status_code: {result.status_code}')
    
    return(lat, lon)    






def wind_barb(cache=None, windspeed_ms=None, direction=None):
    '''create a rotated wind barb for a given windspeed (m/s) and direction
    
    Args:
        cache(`str` or `Path`): path to store files
        windspeed_ms(`float`): windspeed in m/s
        direction(float): wind direction 0 North, 90 East, 180 S
        
    Returns:
        `pathlib.Path()`: path to image barb
    '''
    cache = Path(cache)
    logging.debug('calculating wind barb')
    if not cache:
        logging.warning('no cache available -- returning None')
        return None
    if not isinstance(windspeed_ms, (float, int)) or not isinstance(direction, (float, int)):
        logging.warning(f'TypeError, expected `int` or `float`: windspeed_ms: {type(windspeed_ms)}, direction: {type(direction)}')
        return None
    
    barb_imgs = [ i for i in Path(constants.wind_barbs_path).glob('*.png')]
    barb_imgs.sort()
    # wind barbs are graded in knots -- convert from m/s to knot
    windspeed_kt = convert_units(windspeed_ms, 'm/s', 'knot')
    # round direction to the nearest 5 degrees
    direction = 5 * round(direction/5)
    # windspeed under 1 knot use the null image
    if windspeed_kt < 1:
        img = barb_imgs[0]
    # windspeeds greater than 105 use the warning symbol
    elif windspeed_kt > 105:
        img = barb_imgs[-1]
    # else pull the appropriate item from the index
    else:
        # round up a little bit
        img = barb_imgs[int(windspeed_kt/5+0.5)+1]
        
    rotated_barb_file = Path(f'{img.stem}_{direction}.png')
    rotated_barb_file = cache/rotated_barb_file
    
    if rotated_barb_file.exists():
        logging.debug(f'using cached version at: {rotated_barb_file}')
    else:
        logging.debug(f'caching version at: {rotated_barb_file}')
        pil_img = Image.open(img)
        #wind barb base images are oriented out of the south
        pil_img = pil_img.rotate(angle=-direction-180, fillcolor='white')
        pil_img.save(fp=rotated_barb_file)
    return rotated_barb_file






def process_data(data, meta_data_flat, cache_path):
    '''process a MET Norway Weather Locationforecast 2.0 timeseries list of JSON
        * Add paths for forecast and wind barb images
        * Add units as list for each value [value, unit]
        
    Args:
        data(`list`): list of JSON data
        meta_data_flat(`dict`): flat dictionary containing meta data for each key type
        cache_path('str'): path to store wind barb images
        
    Returns:
        `list` of `dict`'''
    def add_units(d):
        my_details = {}
        for my_detail, my_value in d.items():
            if my_detail in meta_data_flat.keys():
                my_details[my_detail] = (my_value, meta_data_flat[my_detail])
        
        return my_details
    if not isinstance(data, list):
        return {}
    
    cache_path = Path(cache_path)
    out = deepcopy(data)

    # move these into the constants?
    # hour keys to search for
    next_hours = ['next_1_hours', 'next_6_hours', 'next_12_hours']
    
    # wind related keys for adding windbarb
    wind_keys = set(['wind_from_direction', 'wind_speed'])
    
    
    # create a dict of all the symbol_code files with a dict comprehension
    symbol_dict = {i.stem: i for i in Path(constants.symbol_codes_path).glob("*")}
    
    # work through each time series
    for index, each_time in enumerate(out): 
        # convert zulu timedate string into human readable time
        time = dateutil.parser.isoparse(each_time['time'])
        time_string = time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime("%d %h %H:%M")
        out[index]['forecast_time_local'] = time_string
   
        # pull the details dict for processing
        this_details = dictor(each_time, 'data.instant.details')
         
        # add wind barbs
        if wind_keys.issubset(this_details.keys()):
            direction = this_details['wind_from_direction']
            wind_speed = this_details['wind_speed']
            this_details['wind_barb_image'] = wind_barb(cache=cache_path, direction=direction,
                                              windspeed_ms=wind_speed)
    
        # update the return dictionary
        out[index]['data']['instant']['details'].update(add_units(this_details))
        
        # process next_x_hours     
        for hour in next_hours:
            this_hour = dictor(each_time, f'data.{hour}')
            if this_hour:
                this_symbol = dictor(this_hour, 'summary.symbol_code')
                this_detail = dictor(this_hour, 'details')                    
                if this_symbol:
                    if this_symbol in symbol_dict.keys():
                        symbol_code_image = symbol_dict[this_symbol]
                    else:
                        symbol_code_image = None
                    this_hour['summary']['symbol_code_image'] = symbol_code_image
                    # update the dictionary
                    out[index]['data'][hour].update(this_hour)
                    
                # add units to detail for each hour if available, update the dictionary
                if this_detail:
                    out[index]['data'][hour]['details'].update(add_units(this_detail))
 
    return out   






def flatten_json(y):
    '''flatten a json nested dictionary and add the value as a list 
        lookup the orignial key in a lookup dict and add 
        an the lookup value to the list of items
        Courtesy of: https://stackoverflow.com/a/51379007/5530152
    
    Args:
        y(`dict`): nested json to flatten into 1D dictionary
        
    Returns:
        `dict`
        
    '''
    out = {}
    
    def flatten(x, name=''):
        if isinstance(x, dict):
#         if type(x) is dict:
            for a in x:
                flatten(x[a], f"{name}{a}_")
        elif isinstance(x, list):
#         elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, f"{name}{i:03}_")
                i += 1
        elif isinstance(x, tuple):
#         elif type(x) is tuple:
            out[name[:-1]] = x
        else:
            out[name[:-1]] = x

    flatten(y)
    return out






def convert_units(v, u_in, u_out, return_int=False):
    '''convert meterological units:
        known units:
            Temperature: celcius, farenheit, kelvin
            Velocity: m/s, k/h, m/h, knot
            length: mm, inch
    
    Args:
        v(`float`): value to convert
        u_in(`str`): input unit
        u_out(`str`): output unit
        
    Returns:
        `float`'''
    if not isinstance(v, (int, float)):
        logging.warning(f'TypeError: expected int or float: {v}')
        return v
    
    try:
        u_in = u_in.lower()
        u_out = u_out.lower()
    except AttributeError as e:
        logging.warning(f'unknown conversion: {u_in} to {u_out}')
        
    units = {
        'celsius': { 'celsius': v , 'fahrenheit': v*9/5+32, 'kelvin': v + 273.15},
        'fahrenheit': { 'celsius': (v-32)*5/9, 'fahrenheit': v, 'kelvin': (v-32)*5/9 + 273.15},
        'kelvin': { 'celsius': v-273.15, 'fahrenheit': (v - 273.15) * 9/5 + 32, 'kelvin': v},
        'm/s': {'m/s': v, 'k/h': v*3.6, 'm/h': v*2.237, 'knot': v*1.944},
        'k/h': {'m/s': v/3.6, 'k/h': v, 'm/h': v/1.609, 'knot': v/1.852},
        'm/h': {'m/s': v/2.237, 'k/h': v*1.609, 'm/h': v, 'knot': v*1.151},
        'knot': {'m/s': v/1.151, 'k/h': v*1.852, 'm/h': v/1.151, 'knot': v},
        'mm': {'inch': v/25.4, 'mm': v},
        'inch': {'mm': v*25.4, 'inch': v}
    }
    try:
        ret_val = units[u_in][u_out]
    except KeyError:
        logging.warning(f'unknown conversion: {u_in} to {u_out}')
        ret_val = v
    
    if return_int:
        try:
            ret_val = int(ret_val)
        except Exception:
            pass
        
    return ret_val






def post_process(data, self):
    '''convert tuples containing value/unit pairs into strings and convert units where needed 
    and add text, time and location strings
    
    Args:
        data(`dict`): flat dictionary containing key: (value, unit)
    
    Returns:
        `dict`'''
    
    out = {}
    
    # map configuration options to unit conversion dictionary
    unit_dict = {'celsius': self.config['temp_units'].lower(), 
                 'mm': self.config['rain_units'.lower()],
                 'm/s': self.config['windspeed'].lower()}
    
    out.update(constants.text)
    out['time_updated_iso_zulu'] = datetime.datetime.utcnow().isoformat()[:-3] + 'Z'
    out['time_updated_iso_local'] = datetime.datetime.now().isoformat()[:-3]
    out['time_updated_local'] = datetime.datetime.now().strftime('Updated: %d %b, %H:%M')
    out['forecast_location'] = self.config['location_name']
        
    for k, v in data.items():
        if isinstance(v, tuple) and len(v) > 1:
            if v[1] in unit_dict:
                my_unit = unit_dict[v[1]]
                value = convert_units(v[0], v[1], my_unit, True)
            else:
                my_unit = v[1]
                value = v[0]
                
            if my_unit in constants.abreviations:
                abreviation = constants.abreviations[my_unit]
            else:
                abreviation = my_unit
           
        else:
            value = v
            abreviation = ''
        
        if isinstance(value, float):
            value = int(value)
        
        clean_str = f'{value}{abreviation}'
            
            
        
        out[k] = clean_str
    return out
    






def update_function(self):
    '''update_function for met_no Plugin() object to fetch forecast data for a given lat, lon
        multiple met_no plugins can be active with different locations
    
    Requirements:
        self.config(`dict`): {
            'lat': latitude of forecast location (`float`),
            'lon': longitude of forecast location (`float`),
            'temp_units': 'celsius' or 'fahrenheit' (`str`),
            'rain_units': 'mm' or 'inch' (`str`),
            'windspeed': 'm/s', 'm/h', 'knot', 'k/h'
        }
        self.cache(`CacheFiles` object)
        
    Args:
        self(namespace): namespace from plugin object        
    '''
    is_updated = False
    # build out some sample data in the constants file
    data = {}
    priority = 2**15
    
    failure = (is_updated, data, priority)
    
    required_config_options = {'lat': 47.94, 
                               'lon': 106.966, 
                               'location_name': 'Ulaanbaatar, Mongolia',
                               'temp_units': 'celsius',
                               'rain_units': 'mm', 
                               'windspeed': 'm/s'
                              }
    
    for k, v in required_config_options.items():
        if not k in self.config:
            logging.info(f'missing configuration value: {k}')
            logging.info(f'using default value: {v}')
            self.config[k] = v
    
    try:
        forecast = requests.get(f"{constants.yr_endpoint}lat={self.config['lat']}&lon={self.config['lon']}")
    except RequestException as e:
        logging.warning(e)
        return failure
    
    if forecast.status_code == 200:
        if dictor(forecast.json(), 'properties.meta.updated_at'):
            is_updated = True
            priority = self.max_priority
            data = forecast.json()
        else:
            logging.warning(f'incomplete data returned; no forecast available')
    else:
        logging.warning(f'failed to fetch data from {constants.yr_endpoint}: status_code: {forecast.status_code}')
        
    meta_data = dictor(data, 'properties.meta.units')
    timeseries_data = dictor(data, 'properties.timeseries')

    # flatten the meta_data JSON so it can be used in processing the rest of the data
    if meta_data and timeseries_data:
        # flatten the meta_data JSON so it can be used in processing the rest of the data
        meta_data_flat = flatten_json(meta_data)
        timeseries_data = process_data(timeseries_data, meta_data_flat, self.cache.path)
    else:
        return failure
    
    data = timeseries_data    
    data = flatten_json(timeseries_data)
    data = post_process(data, self)
    
    return is_updated, data, priority






# get_coord('Ulaanbaatar, mongolia')






# # coord = get_coord('Den Haag, Netherlands')
# coord = get_coord('Den Haag, Netherlands')
# self = SelfDummy()
# self.config = {'lat': coord[0], 
#                'lon': coord[1], 
#                'location_name': 'Den Haag',
# #                'temp_units': 'knot',
# #                'rain_units': 'inch', 
#                'windspeed': 'knot'
#               }
# self.cache = CacheFiles()


