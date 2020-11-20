# lms_client
![sample image for plugin lms_client](lms_client_sample.png)
```

PLUGIN: lms_client v:0.1.0


FUNCTION: scan_servers
USER FACING HELPER FUNCTION:
    scan local network for LMS servers; print list of servers players for first server
    
    usage:
        --run_plugin_func lms_client.scan_servers
        
    Args:
        None
    Returns:
        None
    
___________________________________________________________________________
 
FUNCTION: update_function
update_function for lms_client provides now-playing LMS information
    
    
    This plugin provides now playing information pulled from a Logitech Media Server 
    and shows now-playing information for a single player multiple players 
    can be tracked by adding multiple plugins sections in the config file
    
    This plugin pulls and displays information from a Logitech Media Server
    instance running on the local network. 
    
    See: 
      * https://mysqueezebox.com/download
    
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
            'player_name': 'LMS Player Name',   # name of player to track
            'idle_timeout': 10,                 # timeout for showing 'pause' screen 
        }
        self.cache(`CacheFiles` object)
            
    Args:
        self(namespace): namespace from plugin object
        
    Returns:
        tuple: is_updated(bool), data(dict), 
    
___________________________________________________________________________
 


SAMPLE CONFIGURATION FOR plugins.lms_client.lms_client

[Plugin: LMS - Your Player Name]
layout = layout
plugin = lms_client
player_name = Your Player Name
min_display_time = 30
max_priority = 0
idle_timeout = 15


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