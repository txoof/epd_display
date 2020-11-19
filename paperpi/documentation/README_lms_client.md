# lms_client
![sample image for plugin lms_client](../documentation/images/lms_client_sample.png)
```

PLUGIN: lms_client v:0.1.0


FUNCTION: scan_servers
scan for and list all available LMS Servers and players on the local network
    
    usage:
        lms_client.scan_servers
        
    Args:
        None
    Returns:
        None
    
___________________________________________________________________________
 
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
 

LAYOUTS AVAILABLE:
  layout
  threeRowLarge
  twoColumn
  twoColumnThreeRows
  twoRowSmall


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.lms_client.lms_client:
   id
   title
   artist
   coverid
   duration
   album_id
   genre
   album
   artwork_url
   coverart
   mode
```