#!/usr/bin/env python3
# coding: utf-8




import logging






import lmsquery
import requests






# # two different import modes for development or distribution
# try:
#     # import from other modules above this level
#     from .layout import layout
# except ImportError:
#     # development in jupyter notebook
#     from layout import layout






try:
    from . import layout
except ImportError:
    import layout






logger = logging.getLogger(__name__)






def update_function(self):
    '''update_function for Plugin() object to read data from a 
        Logitech Media Server and show now-playing information for a single player
        multiple players can be tracked by adding multiple plugins
    
    Requirements:
        self.config(`dict`): {
            'player_name': 'LMS Player Name',   # name of player to track
            'idle_timeout': 10,                 # timeout for showing 'pause' screen 
        }'''
    now_playing = None
    data = {
        'id': 0,
        'title': 'Err: No Player',
        'artist': 'Err: No Player',
        'coverid': 'Err: No Player',
        'duration': 0,
        'album_id': 'Err: No Player',
        'genre': 'Err: No Player',
        'album': 'Err: No Player',
        'artwork_url': 'Err: No Player',
        'mode': 'None'
    }

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




