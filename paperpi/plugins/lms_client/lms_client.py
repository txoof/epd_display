#!/usr/bin/env python3
# coding: utf-8






import logging






import lmsquery
import requests
from epdlib.Screen import Update
from copy import copy






import QueryLMS






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
except ImportError:
    import layout
    import constants






logger = logging.getLogger(__name__)






def update_function(self):
    '''update_function for Plugin() object to read data from a 
    Logitech Media Server and show now-playing information for a single player
    multiple players can be tracked by adding multiple plugins
    
    Requirements:
        self.config(`dict`): {
            'player_name': 'LMS Player Name',   # name of player to track
            'idle_timeout': 10,                 # timeout for showing 'pause' screen 
        }
        self.cache(`CacheFiles` object)
            
    Args:
        self(namespace): namespace from plugin object
    %U'''
    def build_lms():
        logging.debug(f'building LMS Query object for player: {player_name}')
#         self.my_lms = lmsquery.LMSQuery(player_name=player_name)
        self.my_lms = QueryLMS.QueryLMS(player_name=player_name)
    
    logging.debug(f'update_function for plugin {self.name}, version {constants.version}')
    now_playing = None
    # make a shallow copy to make updates possible without impacting origonal obj.
    data = copy(constants.data)
    is_updated = False
    priority = 2**15    
 
    
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
#         logging.debug(f'building LMS Query object for player: {player_name}')
#         self.my_lms = lmsquery.LMSQuery(player_name=player_name)
        build_lms()
    try:
        # fetch the now playing data for the player
        now_playing = self.my_lms.get_now_playing()
        # remove the time key to make comparisions now_playing data updates easier in the Plugin class
        if 'time' in now_playing:
            now_playing.pop('time')
    
    # this should cover most network related errors
    except requests.exceptions.ConnectionError as e:
        logging.error(f'network error finding player "{player_name}": {e}')
        logging.info(f'rebuilding LMS Query object for {player_name}')
        build_lms()
        return failure
    # if no data is returned, pulling 'time' key throws key error
    except KeyError as e:
        logging.warning(f'error getting now plyaing information for "{player_name}": KeyError {e}')
        logging.warning('this error is typical of newly added player or player that has no "now playing" data')
        return failure
    # QueryLMS throws ValueError if player_id is not set 
    except ValueError as e:
        logging.warning(f'could not get now playing information for "{player_name}": ValueError {e}')
        logging.warning(f'check player_name in config file. Is "{player_name}" connected to the LMS server?')
        return failure
    
    
    
    # process the now_playing state and set priority, update and data
    if now_playing:
        data = now_playing
        try:
            data['coverart'] = self.cache.cache_file(now_playing['artwork_url'], 
                                                     now_playing['album_id'])
        except KeyError as e:
            logging.warning(f'failed to cache file -- now_playing data did not contain complete data: {e}')
    logging.debug(f'now_playing: {now_playing["mode"]}')
    if now_playing['mode'] == 'play':
        if self.data == data:
            priority = self.max_priority
        else:
            priority = self.max_priority - 1
        self.play_state = 'play'
        is_updated = True
        
    elif now_playing['mode'] == 'pause':
        # moving from play to pause, decrease priority and refresh idle_timer
        if self.play_state == 'play':
            self.idle_timer.update()
            priority = self.max_priority + 1
            self.play_state = 'pause'
        
        # if the idle timer has expired, decrease priority
        if self.idle_timer.last_updated > self.config['idle_timeout']:
            priority = self.max_priority + 3
            self.play_state = 'pause'
        else:
            priority = self.max_priority + 1

        is_updated = True
    
    else: 
        self.play_state = now_playing['mode'] 
        priority = 2**15
        is_updated = False
    logging.info(f'priority set to: {priority}')
    return (is_updated, data, priority)






# from SelfDummy import SelfDummy
# from CacheFiles import CacheFiles


# logger.root.setLevel('DEBUG')
# logging.debug('foo')

# self = SelfDummy()
# self.max_priority = 0
# self.config = {'player_name': 'slimpi',
#                'idle_timeout': 5}
# self.cache = CacheFiles()






# u, d, p = update_function(self)
# if u != self.data:
#     self.data = d
# print(f'idle timer: {self.idle_timer.last_updated}, idle_timeout {self.config["idle_timeout"]}')
# print(p)
# print(d)






def scan_servers(*args, **kwargs):
    """scan local network for LMS servers; print list of servers players for first server
    
    usage:
        --run_plugin_func lms_client.scan_servers
        
    Args:
        None
    Returns:
        None
    %U"""
    print(f'Scanning for available LMS Server and players')
    servers = QueryLMS.QueryLMS().scan_lms()
    if not servers:
        print('Error: no LMS servers were found on the network. Is there one running?')
        do_exit(1)
    print('servers found:')
    print(servers)
    players = QueryLMS.QueryLMS().get_players()
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
















