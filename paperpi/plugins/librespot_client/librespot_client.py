#!/usr/bin/env python3
# coding: utf-8




import logging






import requests






try:
    from . import layout
except ImportError:
    import layout






def update_function(self):
    data = {
        'title': 'Err: no data',
        'artist': 'Err: no data',
        'album': 'Err: no data',
        'artwork_url': 'Err: no data',
        'duration': 0,
        'player': 'Err: no data',
        'mode': 'None'}
    priority = -1
    is_updated = False
    
    failure = (is_updated, data, priority)
#     logging.info('creating libre-spot spotify plugin (Spocon)')
    logging.debug(f'fetching access token from librespot player {self.config["player_name"]}')
    logging.debug(f'requesting access scope: {constants_spot.spot_scope}')
    
    # add the property play_state for recording current play state 
    if not hasattr(self, 'play_state'):
        self.play_state = 'None'
    
    # add the idle timer on first run
    if not hasattr(self, 'idle_timer'):
        logging.debug(f'adding idle_timer of class `Update()`')
        self.idle_timer = Update()    
    
    if not self.cache:
        self.cache = CacheFiles(path_prefix=self.config['player_name'])
        
        
    try:
        token = requests.post(constants_spot.libre_token_url)
    except requests.ConnectionError as e:
        logging.error(f'Failed to pull Spotify token from librespot at url: {constants_spot.libre_token_url}')
        logging.error(f'{e}')
        return failure
    
    if token.status_code == 200:
        logging.debug('token received')
        try:
            headers = {'Authorization': 'Bearer ' + token.json()['token']}
        except JSONDecodeError as e:
            logging.error(f'failed to decode token JSON object: {e}')
            return failure
    else:
        logging.info(f'no token available from librespot status: {token.status_code}')
        return failure
    
    # use the token to fetch player information from spotify
    if 'Authorization' in headers:
        player_status = requests.get(constants_spot.spot_player_url, headers=headers)
    else:
        logging.warning(f'no valid Authroization token found in response from librespot: {headers}')
        return failure
    
    if player_status.status_code == 200:
        try:
            player_json = player_status.json()
        except JSONDecodeError as e:
            logging.error(f'failed to decode player status JSON object: {e}')
            return failure
        
        # bail out if the player name does not match
        if not dictor(player_json, 'device.name') == self.config['player_name']:
            logging.info(f'{self.config["player_name"]} is not active: no data')
            return failure
        
        # map json data to dictionary format that Layout() objects can use
        # probably should wrap this in a try:
        for key in constants_spot.spot_map:
            data[key] = dictor(player_json, constants_spot.spot_map[key])
            
        if 'artwork_url' in data and 'id' in data:
            data['coverart'] = self.cache.cache_file(url=data['artwork_url'], file_id=data['id'])
                
        playing = dictor(player_status.json(), 'is_playing')
        if playing is True:
            data['mode'] = 'play'
            is_updated = True
            self.play_state = 'play'
            priority = self.max_priority 
        elif playing is False:
            data['mode'] = 'paused'
            if self.play_state == 'play':
                logging.debug('resetting idle_timer')
                self.idle_timer.update()
            if self.idle_timer.last_updated > self.config['idle_timeout']:
                priority = self.max_priority + 2
            else:
                priority = self.max_priority + 1
            is_updated = True
            self.play_state = 'paused'
        else:
            data['mode'] = None            
            is_updated = True
            priority = -1    
            self.play_state = 'None'
    
    return (is_updated, data, priority)




