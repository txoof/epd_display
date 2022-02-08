#!/usr/bin/env python3
# coding: utf-8

try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants
    
from pathlib import Path
from requests import get
import logging

logger = logging.getLogger(__name__)

def callHome(url, apiToken):
    headers = {
        "Authorization": f'Bearer {apiToken}',
        "content-type": "application/json",
    }

    response = get(url, headers=headers)
    entity_json = response.json()
    return entity_json


def updateSensor(self, sensorId):
    sensorText = 'Sensor failure'
    try:
        sensorConfigId = self.config[f'entity{sensorId}_id']
        entityJson = callHome(f'{self.config["home_assistant_basepath"]}/api/states/{sensorConfigId}', self.config['home_assistant_token'])
        entity_name = self.config[f'entity{sensorId}_name']
        entity_value = entityJson['state']
        entity_unit = entityJson['attributes']['unit_of_measurement']
        sensorText = f'{entity_name} : {entity_value}{entity_unit}'
    except Exception as e:
        logging.error(f'Failed to fetch sensor values: {e}')

    return sensorText

def updatePlayer(self):
    player = {
        'media_title': ' ',
        'media_artist': ' ',
        'image': Path(constants.img_file).resolve(),
        'media': 'Nothing is playing...',
        'priority': self.max_priority
    }

    try:
        mediaJson = callHome(f'{self.config["home_assistant_basepath"]}/api/states/{self.config["media_id"]}', self.config['home_assistant_token'])
        if mediaJson['state'] == 'playing':
            media_content_id = mediaJson["attributes"]["media_content_id"]
            media_picture = mediaJson['attributes']['entity_picture_local']
            file_id = f'{constants.private_cache}/{media_content_id}'
            player['image'] = self.cache.cache_file(url=f'{self.config["home_assistant_basepath"]}{media_picture}', file_id=file_id)
            player['media_title'] = mediaJson['attributes']['media_title']
            player['media_artist'] = mediaJson['attributes']['media_artist']
            player['media'] = 'Currently playing...'
            if self.media_content_id != media_content_id:
                player['priority'] = self.max_priority - 1
                self.media_content_id = media_content_id
    except Exception as e:
        logging.error(f'Failed to fetch media player: {e}')
        player['media'] = 'Failed to fetch data'

    return player


def update_function(self, *args, **kwargs):
    '''update function for home assistant plugin
    
    This plugin connects to home assistant and can fetch four sensor values of choice as well as
    displaying what is currently playing on a select media player
    
    Requirements:
        self.config(dict): {
            'home_assistant_basepath': 'base url to home assistant',
            'home_assistant_token': 'authentication token for home assistant',
            'entity1_name': 'display name for sensor 1',
            'entity1_id': 'home assistant id for sensor 1',
            'entity2_name': 'display name for sensor 2',
            'entity2_id': 'home assistant id for sensor 2',
            'entity3_name': 'display name for sensor 3',
            'entity3_id': 'home assistant id for sensor 3',
            'entity4_name': 'display name for sensor 4',
            'entity4_id': 'home assistant id for sensor 4',
            'media_id': 'home assistant media player id'
        }
        
    Args: 
        self(namespace): namespace from plugin object
    
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))

    %U'''   
   
    if not hasattr(self, 'media_content_id'):
        self.media_content_id = ''
   
    entity1 = updateSensor(self, '1')
    entity2 = updateSensor(self, '2')
    entity3 = updateSensor(self, '3')
    entity4 = updateSensor(self, '4')
    player  = updatePlayer(self)
    
    # build the output
    is_updated = True
    data = {
        'entity1': entity1,
        'entity3': entity3,
        'entity2': entity2,
        'entity4': entity4,
        'media': player['media'],
        'title': player['media_title'],
        'artist': player['media_artist'],
        'image': player['image']
    }
    
    self.cache.remove_stale(d=constants.expire_cache, path=constants.private_cache)
    
    return (is_updated, data, player['priority'])

