# mod_name
![sample image for plugin <module 'plugins.lms_client' from '/home/pi/src/epd_display/paperpi/plugins/lms_client/__init__.py'>](../documentation/images/lms_client_sample.png)
```

FUNCTION: update_function
update_function for Plugin() object to read data from a 
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
    
___________________________________________________________________________
 
```