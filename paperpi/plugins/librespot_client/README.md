# librespot_client
![sample image for plugin librespot_client](plugins/librespot_client/librespot_client_sample.png)
```

PLUGIN: librespot_client v:0.1.0


FUNCTION: update_function
update function for librespot_client provides now-playing Spotify information
    
    This plugin pulls and displays information from a Librespot-Java instance running
    on the same host. SpoCon is a debian package that installs and configures
    the Librespot service easily.
    
    See: 
      * https://github.com/librespot-org/librespot-java
      * https://github.com/spocon/spocon -- Raspbian package of librespot

    
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
        'player_name': 'SpoCon-Player',   # name of player to track
        'idle_timeout': 10,               # timeout for disabling plugin
    }
    self.cache(`CacheFiles` object)

    Args:
        self(namespace): namespace from plugin object
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))        
    
___________________________________________________________________________
 


SAMPLE CONFIGURATION FOR plugins.librespot_client.librespot_client

[Plugin: Librespot]
layout = layout
plugin = librespot_client
max_priority = 0
min_display_time = 15
# name of librespot player
player_name = SpoCon-Spotify
# time in seconds before plugin is removed from the display loop
idle_timeout = 10


LAYOUTS AVAILABLE:
  layout
  threeRowLarge
  twoColumn
  twoColumnThreeRows
  twoRowSmall


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.librespot_client.librespot_client:
   title
   artist
   album
   artwork_url
   duration
   player
   mode
```

