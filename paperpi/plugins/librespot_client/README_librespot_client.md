# librespot_client
![sample image for plugin librespot_client](plugins/librespot_client/librespot_client_sample.png)
```

PLUGIN: librespot_client v:0.1.0


FUNCTION: update_function
update function for librespot_client provides now-playing information
    from a librespot-java service running locally
    
    See: 
      * https://github.com/librespot-org/librespot-java
      * https://github.com/spocon/spocon -- Raspbian package of librespot
    
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