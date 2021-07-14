#!/usr/bin/env python3
# coding: utf-8






import logging






import requests
from epdlib.Screen import Update
from dictor import dictor
from copy import copy






try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants






logger = logging.getLogger(__name__)






def update_function(self):
    '''update function for librespot_client provides now-playing Spotify information
    
    This plugin pulls and displays information from a Librespot-Java instance running
    on the same host. SpoCon is a debian package that installs and configures
    the Librespot service easily.
    
    See: 
      * https://github.com/librespot-org/librespot-java
      * https://github.com/spocon/spocon -- Raspbian package of librespot

    
    This plugin dynamically changes the priority depending on the status of the librespot
    player. Remember, lower priority values are considered **more** important
    Condition         Priority
    ------------------------------
    playing           max_priority
    track change      max_priority -1
    paused            max_priority +1
    stopped           max_priority +3
    non-functional    32,768 (2^15)

      
    Requirements:
        self.config(`dict`): {
        'player_name': 'SpoCon-Player',   # name of player to track
        'idle_timeout': 10,               # timeout for disabling plugin
    }
    self.cache(`CacheFiles` object)

    Args:
        self(namespace): namespace from plugin object
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))        
    %U'''
    logging.debug(f'update_function for plugin {self.name}, version {constants.version}')    
    is_updated = False
    # make a shallow copy so the data object can be updated through the procedure
    data = copy(constants.data)
    priority = 2**15
    failure = (is_updated, data, priority)

    # add a play_state attribute
    if not hasattr(self, 'play_state'):
        self.play_state = 'None'
    
    # add the idle timer on first run
    if not hasattr(self, 'idle_timer'):
        logging.debug(f'adding idle_timer of class `Update()`')
        self.idle_timer = Update()    
        
    # fetch token    
    logging.debug(f'fetching API access token from librespot player {self.config["player_name"]}')
    logging.debug(f'requesting spotify API access scope: {constants.spot_scope}')        
    try:
        token = requests.post(constants.libre_token_url)
    except requests.ConnectionError as e:
        logging.error(f'cannot proceed: failed to pull Spotify token from librespot at url: {constants.libre_token_url}')
        logging.error(f'{e}')
        return failure
    # check token
    logging.debug('checking API access token')
    if token.status_code == 200:
        logging.debug('token OK')
        try:
            headers = {'Authorization': 'Bearer ' + token.json()['token']}
        except JSONDecodeError as e:
            logging.error(f'failed to decode token JSON object: {e}')
            return failure
    else:
        logging.info(f'cannot proceed: no token available from librespot status: {token.status_code}')
        return failure
    
    # use the token to fetch player information from spotify
    logging.debug('fetch player status from Spotify')
    if 'Authorization' in headers:
        try:
            player_status = requests.get(constants.spot_player_url, headers=headers)
        except requests.exceptions.RequestException as e:
            logging.info(f'failed to get player status: {e}')
            player_stats = None
    else:
        logging.error(f'cannot proceed: no valid Authroization token found in response from librespot: {headers}')
        return failure    
    
    logging.debug('checking player_status')
    if player_status.status_code == 200:
        try:
            logging.debug('gathering json data')
            player_json = player_status.json()
        except JSONDecodeError as e:
            logging.error(f'cannot proceed: failed to decode player status JSON object: {e}')
            return failure
                
        # bail out if the player name does not match
        if not dictor(player_json, 'device.name').lower() == self.config['player_name'].lower():
            logging.info(f'{self.config["player_name"]} is not active: no data')
            return failure
    else:
        logging.info(f'{self.config["player_name"]} does not appear to be available')
        return failure
        
    # map spotify keys to local values
    for key in constants.spot_map:
        data[key] = dictor(player_json, constants.spot_map[key])

    if 'artwork_url' in data and 'id' in data:
        # set the file_id to use the private cache
        file_id = f'{constants.private_cache}/{data["id"]}'
#         data['coverart'] = self.cache.cache_file(url=data['artwork_url'], file_id=data['id'])
        data['coverart'] = self.cache.cache_file(url=data['artwork_url'], file_id=file_id)

    playing = dictor(player_status.json(), 'is_playing')
    if playing is True:
        logging.debug(f'{self.config["player_name"]} is playing')
        data['mode'] = 'play'
        # if the data has not changed, keep priority; else, bump the priority 
        if self.data == data:
            logging.debug('data matches')
            priority = self.max_priority
        else:
            logging.debug('data does not match')
            priority = self.max_priority - 1
            
        self.play_state = 'play'
        is_updated = True
        
    elif playing is False:
        data['mode'] = 'pause'
        ## moving from "play" to "pause", decrease priority
        if self.play_state == 'play':
            self.idle_timer.update()
            priority = self.max_priority + 1
        
        # if the idle timer has expired, decrease priority
        if self.idle_timer.last_updated > self.config['idle_timeout']:
            priority = self.max_priority + 3
        else:
            priority = self.max_priority + 1

        self.play_state = 'pause'        
        is_updated = True
        
    else:
        self.plays_state = None
        data['mode'] = None
        priority = 2**15
        is_updated = False
    
    # clean stale data out of cache
#     self.cache.remove_stale(d=constants.expire_cache)
    self.cache.remove_stale(d=constants.expire_cache, path=constants.private_cache)
    
    logging.info(f'priority set to: {priority}')
    return is_updated, data, priority






# logging.root.setLevel('DEBUG')






# # use this for testing
# from SelfDummy import SelfDummy
# from CacheFiles import CacheFiles
# from epdlib import Layout
# self = SelfDummy()
# self.max_priority = 0
# self.config = {'player_name': 'Spocon-Spotify',
#                'idle_timeout': 5}
# self.cache = CacheFiles()






# dir_path = '.'
# my_l = {
#     'title': {
#         'image': False,
#         'max_lines': 3,
#         'padding': 0,
#         'width': 1,
#         'height': .70,
#         'abs_coordinates': (0, 0),
#         'hcenter': True,
#         'vcenter': True,
#         'align': 'left',
#         'relative': False,
#         'mode': 'L',
#         'font': dir_path+'/../../fonts/Oswald/static/Oswald-Medium.ttf'
#     },
#     'artist': {
#         'image': False,
#         'max_lines': 2,
#         'width': 1,
#         'height': .20,
#         'abs_coordinates': (0, None),     
#         'hcenter': True,
#         'vcenter': True,
#         'relative': ['artist', 'title'],
#         'mode': 'L',
#         'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf'
#     },
#     'album': {
#         'image': False,
#         'max_lines': 1,
#         'width': 1,
#         'height': .1,
#         'abs_coordinates': (0, None),
#         'hcenter': True,
#         'vcenter': True,
#         'relative': ['album', 'artist'],
#         'mode': 'L',
#         'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf'
#     },     
# }






# l = Layout(resolution=(1200, 800))
# l.layout = my_l






# # test layouts with this code snip
# u, d, p = update_function(self)
# # if u != self.data:
# self.data = d
# print(f'idle timer: {self.idle_timer.last_updated}, idle_timeout {self.config["idle_timeout"]}')
# print(p)
# print(d)
# # print('*'*50)
# # print(self.data)


# logging.root.setLevel('DEBUG')


# l.update_contents(d)
# l.concat()















