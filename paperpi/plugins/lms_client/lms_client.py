#!/usr/bin/env python3
# coding: utf-8






import logging






import lmsquery
import requests
from epdlib.Screen import Update






import sys
from pathlib import Path






# # two different import modes for development or distribution
# try:
#     # import from other modules above this level
#     from .layout import layout
# except ImportError:
#     # development in jupyter notebook
#     from layout import layout






try:
    from . import layout
    from . import constants
    from . import my_help
except ImportError:
    import layout
    import constants
    import my_help






logger = logging.getLogger(__name__)






def update_function(self):
    '''update_function for Plugin() object to read data from a 
        Logitech Media Server and show now-playing information for a single player
        multiple players can be tracked by adding multiple plugins
    
    Requirements:
        self.config(`dict`): {
            'player_name': 'LMS Player Name',   # name of player to track
            'idle_timeout': 10,                 # timeout for showing 'pause' screen 
            
    Args:
        self(namespace): namespace from plugin object
        
        }'''
    logging.debug(f'update_function for plugin {self.name}, version {constants.version}')
    now_playing = None
    data = constants.data

    is_updated = False
    priority = -1
    
    failure = (is_updated, data, priority)
    
    player_name = self.config['player_name']
    
    if not hasattr(self, 'play_state'):
        self.play_state = 'None'
    
    # add the idle timer on first run
    if not hasattr(self, 'idle_timer'):
        logging.debug(f'adding idle_timer of class `Update()`')
        self.idle_timer = Update()
    
    # check if LMS Query object is initiated
    if not hasattr(self, 'my_lms'):
        # add LMSQuery object to self
        logging.debug(f'building LMS Query object for player: {player_name}')
        self.my_lms = lmsquery.LMSQuery(player_name=player_name)
    try:
        # fetch the now playing data for the player
        now_playing = self.my_lms.now_playing()
        # remove the time key to make comparisions now_playing data updates easier in the Plugin class
        if 'time' in now_playing:
            now_playing.pop('time')
            
    except requests.exceptions.ConnectionError as e:
        logging.error(f'could not find player "{player_name}": {e}')
        return failure
    except KeyError as e:
        logging.warning(f'error getting now plyaing information for "{player_name}": KeyError {e}')
        logging.warning('this error is typical of newly added player or player that has no "now playing" data')
        return failure
    
    if now_playing:
        data = now_playing
        try:
            data['coverart'] = self.cache.cache_file(now_playing['artwork_url'], 
                                                     now_playing['album_id'])
        except KeyError as e:
            logging.warning(f'failed to cache file -- now_playing data did not contain complete data: {e}')
    
    # set the priority based on play state
    logging.debug(f'play_state before checking now_playing: {self.play_state}')
    if now_playing['mode'] == 'play':
        priority = self.max_priority
        is_updated = True
        self.play_state = now_playing['mode']
    elif now_playing['mode'] == 'pause':
        # if switching from play to pause, refresh the idle timer
        if self.play_state == 'play':
            logging.debug('resetting idle_timer')
            self.idle_timer.update()
        if self.idle_timer.last_updated > self.config['idle_timeout']:
            priority = self.max_priority + 2
        else:
            priority = self.max_priority + 1
        is_updated = True
        self.play_state = now_playing['mode']
    else:
        priority = -1
        is_updated = False
        play_state = now_playing['mode']
    
    logging.debug(f'current priority: {priority}, current play state: {self.play_state}')
    return (is_updated, data, priority)






def scan_servers():
    """scan for and list all available LMS Servers and players on the local network
    
        to use, run: $ paperpi -m lms_client.scan_servers"""
    print(f'Scanning for available LMS Server and players')
    servers = lmsquery.LMSQuery().scanLMS()
    if not servers:
        print('Error: no LMS servers were found on the network. Is there one running?')
        do_exit(1)
    print('servers found:')
    print(servers)
    players = lmsquery.LMSQuery().get_players()
    # print selected keys for each player
    keys = ['name', 'playerid', 'modelname']
    for p in players:
        print('players found:')
        try:
            for key in keys:
                print(f'{key}: {p[key]}')
            print('\n')
        except KeyError as e:
            pass 






# def my_help(func=None):
#     '''Print help for this plugin
    
#     Args:
#         func(`string`): name of function '''
#     import types
#     if not func:
#         l = [f for f in globals().values() if type(f) == types.FunctionType]
#         print('*'*50)        
#         print('Available functions in this plugin:')
#         for i in l:
#             print(f'##### {i.__name__} #####')
#             print(f'{i.__doc__}\n\n')
        
#         print('*'*50)
#         print('Available Layouts:')
#         for name in vars(layout).keys():
#             if not name.startswith('__') and not name in ('os', 'dir_path'):
#                 print(f'  {name}')
        
#         print('*'*50)
#         print('data dictionary keys available for layouts:')
#         for k in constants.data:
#             print(f'   {k}')
            
#     else:
#         print(f'{func.__doc__}')
    






# def my_help(func=None):
#     '''Print docstrings for all available functions within this module'''
#     import types
#     if not func:
#         l = [f for f in globals().values() if type(f) == types.FunctionType]
#         print('Available functions in this plugin:')
#         for i in l:
#             print(f'{i.__doc__}')
#     else:
#         print(f'{func.__doc__}')
        






# update_function(self)











