# mod_name
![sample image for plugin lms_client](../documentation/images/lms_client_sample.png)
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