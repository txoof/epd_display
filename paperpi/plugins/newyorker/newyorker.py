#!/usr/bin/env python3
# coding: utf-8








import logging






from random import randrange
from datetime import datetime
from pathlib import Path






# two different import modes for development or distribution
try:
    # import from other modules above this level
    from . import layout
    from . import constants
except ImportError:
    import constants
    # development in jupyter notebook
    import layout






import feedparser
import requests






logger = logging.getLogger(__name__)






def update_function(self, **kwargs):
    '''update function for newyorker provides a New Yorker comic of the day
    
    This plugin provides an image and text pulled from the New Yorker 
    
    Requirments:
        self.config(dict): {
            'day_range': 'number of days to pull comics from (default: 5)',
        }    
    
    Args:
        self(`namespace`)
        day_range(`int`): number of days in the past to pull radom comic and text from
            use 1 to only pull from today
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))    
    %U'''
    def time_now():
        return datetime.now().strftime("%H:%M")

    def fetch_comic(day_range=1):
        '''pull a feed from the New Yorker and choose an comic at random from the specified range
        
             cache the image to show again later to limit network trafic
             
        Args:
            day_range(int): number of days to choose from (use 1 for today only)
            
        Returns:
            tuple: (bool, dict) - True if successful, dictionary of comic, caption and time'''
        # set up the feed parser and fetch the feed
        feed = feedparser.parse(constants.feed_url)
        if feed.has_key('bozo_exception'):
            logging.warning(f'could not fetch feed for {constants.feed_url}')
            # bail out if there was an error
            return(False, {})

        if day_range > len(feed.entries):
            day_range = len(feed.entries)
            logging.warning(f'day_range set to a value larger than the number of entries returned by the feed. Setting to: {day_range} ')        

        logging.debug(f'choosing a comic from the last {day_range} days')
        choice = randrange(0, day_range)

        try:
            comic_caption = feed.entries[choice].summary
            comic_url = feed.entries[choice].media_thumbnail[0]['url']
            comic_id = feed.entries[choice].id
        except IndexError as e:
            logging.warning(f'no valid data was returned in the feed: {e}')        
            return(False, {}, day_range)
        except KeyError as e:
            logging.warning(f'no url was found under the `media_thumbnail`: {e}')
            return(False, {}, day_range)

        comic_id = f'{constants.private_cache}/{comic_id}'
        comic_image = self.cache.cache_file(url=comic_url, file_id=comic_id)

        return(True, {'comic': comic_image, 
                      'caption': comic_caption, 
                      'time': time_now()}, day_range)    
            
    success = False
    is_updated = True
    
    data = {'comic': Path(constants.images_path)/'shruggy.jpg',
            'caption': f'Could not load a comic. Are the Inter-Tubes clogged?',
            'time': time_now()
            }
    try:
        day_range = self.config['day_range']
    except KeyError as e:
        logging.warning(f'module is not properly configured and is missing keys: {e}')
        data['caption'] = f'The New Yorker plugin configuration is missing "{e.args[0]}" setting'
    else:
        success, my_data, day_range = fetch_comic(day_range)  

    priority = self.max_priority
    
    if success:
        data.update(my_data)
        
    logging.debug(f'data: {data}')
    
    self.cache.remove_stale(d=day_range, path=constants.private_cache)
    
    return (is_updated, data, priority) 








# logger = logging.getLogger(__name__)
# logger.root.setLevel('DEBUG')






# from library.CacheFiles import CacheFiles
# # def test_plugin():
# '''This code snip is useful for testing a plugin from within Jupyter Notebook'''
# from library import Plugin
# from IPython.display import display
# # this is set by PaperPi based on the configured screen
# test_plugin = Plugin(resolution=(1200, 800))
# # this is pulled from the configuration file; the appropriate section is passed
# # to this plugin by PaperPi during initial configuration
# test_plugin.config = {'day_range': 20}
# test_plugin.layout = layout.layout
# # this is done automatically by PaperPi when loading the plugin
# test_plugin.cache = CacheFiles()
# test_plugin.update_function = update_function
# test_plugin.refresh_rate = 1
# # display(test_plugin.image)
# # return test_plugin
# # my_plugin = test_plugin






# test_plugin.update()
# test_plugin.image




