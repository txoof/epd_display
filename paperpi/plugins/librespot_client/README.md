# librespot_client
![sample image for plugin paperpi.plugins.librespot_client](./librespot_client.layout-sample.png) 

```
 
PLUGIN: librespot_client v:0.2.1

 
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
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.librespot_client.librespot_client

[Plugin: Librespot]
layout = layout
plugin = librespot_client
refresh_rate = 10
max_priority = 0
min_display_time = 15
# name of librespot player
player_name = SpoCon-Spotify
# time in seconds before plugin is removed from the display loop
idle_timeout = 10

 
LAYOUTS AVAILABLE:
  layout
  three_rows_text_only
  two_column_three_row
  two_rows_text_only
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.librespot_client.librespot_client:
   title
   artist
   album
   artwork_url
   duration
   player
   mode
```

## Provided Layouts:

layout: **layout**

![sample image for plugin layout](./librespot_client.layout-sample.png) 


layout: **three_rows_text_only**

![sample image for plugin three_rows_text_only](./librespot_client.three_rows_text_only-sample.png) 


layout: **two_column_three_row**

![sample image for plugin two_column_three_row](./librespot_client.two_column_three_row-sample.png) 


layout: **two_rows_text_only**

![sample image for plugin two_rows_text_only](./librespot_client.two_rows_text_only-sample.png) 


## Additional librespot_client information
### HiFiBerry Sound Card
Adding a HiFiBerry DAC+ or DAC+ Pro sound card to your Raspberry Pi can dramatically improve the sound output. Add a [SqueezeLite](#squeezelite) player to PaperPi and you have a full featured media player with a beautiful Screen.
![./lms_client_sample.png]

[HiFiBerry hats](https://www.hifiberry.com/shop/#boards) such as the DAC+, DAC+ Pro or DAC2 Pro are great choices if you intend to play the audio out to an amplifier or other powered speaker. Choose a HiFiBerry Amp2 or similar if you want to attach speakers directly to the the Pi. Make sure you buy a HiFi Berry with the 2x20 male header or add one. The WaveShare display must have access to the GPIO pins.

Follow [HiFiBerry's excellent guide](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/) for installing and configuring the sound card.

### librespot-java & SpoCon
[librespot-java](https://github.com/librespot-org/librespot-java) is required for this plugin. The java implementation offers a local web interface that this plugin depends on for pulling now-playing information.

[SpoCon](https://github.com/spocon/spocon) provides an easy-install Raspbian package for intalling librespot-java.

Once you've installed and configured your SpoCon service, you will need to set up the plugin in your `paperpi.ini` configuration.
```
[Plugin: My LibreSpot Player]
layout = layout
plugin = librespot_client
refresh_rate = 10
# 0 is a good choice for music service tracking to ensure the currently
# playing music is displayed
max_priority = 0
# anything less than 15 seconeds is probably not useful
min_display_time = 15
# name of librespot player
player_name = SpoCon-Spotify
# time in seconds before plugin is removed from the display loop when not playing
idle_timeout = 10
```