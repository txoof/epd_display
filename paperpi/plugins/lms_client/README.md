# lms_client
![sample image for plugin lms_client](./lms_client_sample.png)
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
update function for lms_client provides now-playing LMS information
    
    
    This plugin provides now playing information pulled from a Logitech Media Server 
    and shows now-playing information for a single player multiple players 
    can be tracked by adding multiple plugins sections in the config file
    
    This plugin pulls and displays information from a Logitech Media Server (LMS)
    instance running on the local network and displays information for a single player.
    
    It is possible to specify this plugin multiple times in the configuration file
    to track different players.
    
    
    For more information on running an Server and Player instance See:
      * General Logitech Media Server information
          - https://mysqueezebox.com/download
      * Slim Devices LMS page
          - http://wiki.slimdevices.com/index.php/Logitech_Media_Server
      * Creating an LMS server on a Raspberry PI
          - https://homehack.nl/creating-a-raspberry-pi-squeezebox-server/
      * SqueezeLite - headless LMS player (this works great with a HiFi Berry DAC+)
          - http://wiki.slimdevices.com/index.php/Squeezelite
      
    
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
        tuple: (is_updated(bool), data(dict), priority(int))
    
___________________________________________________________________________
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.lms_client.lms_client

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
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.lms_client.lms_client:
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

## Additional lms_client information
### HiFiBerry Sound Card
Adding a HiFiBerry DAC+ or DAC+ Pro sound card to your Raspberry Pi can dramatically improve the sound output. Add a [SqueezeLite](#squeezelite) player to PaperPi and you have a full featured media player with a beautiful Screen.
![./lms_client_sample.png]

[HiFiBerry hats](https://www.hifiberry.com/shop/#boards) such as the DAC+, DAC+ Pro or DAC2 Pro are great choices if you intend to play the audio out to an amplifier or other powered speaker. Choose a HiFiBerry Amp2 or similar if you want to attach speakers directly to the the Pi. Make sure you buy a HiFi Berry with the 2x20 male header or add one. The WaveShare display must have access to the GPIO pins.

Follow [HiFiBerry's excellent guide](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/) for installing and configuring the sound card.


<a Name="squeezelite"></a>
### SqueezeLite
[SqueezeLite](http://wiki.slimdevices.com/index.php/Squeezelite) adds a headless player to your Raspberry Pi. SqueezeLite players can be controlled through a local web interface or via a variety of [Android](https://play.google.com/store/search?q=squeezebox) and [iOS](https://www.apple.com/nl/search/squeezebox?src=globalnav) applications. 

If you intend to use other audio output software such as a Spotify Player (e.g. librespot), you may want to set SqueezeLite to close the output device when it is not playing. Adding `SB_EXTRA_ARGS="-C 10"` to `/etc/default/squeezelite/squeezelite` will close the audio device after 10 seconds freeing it for other applications.

Once you've installed and configured your SqueezeLite player to locate your server and chceck the player name use:

```
$ paperpi --run_plugin_func lms_client.scan_servers
Scanning for available LMS Server and players
servers found:
[{'host': '192.168.178.9', 'port': 9000}]
players found:
name: slimpi
playerid: dc:a6:32:29:99:f0
modelname: SqueezeLite


players found:
name: MacPlay
playerid: 68:5b:35:b5:97:bf
modelname: SqueezePlay
```

Use this information to configure the lms_client plugin to show one or more players. Create a new plugin for each additional player.
```
[Plugin: LMS MacPlay]
layout = twoColumnThreeRows
plugin = lms_client
# keep this around 5-30 to prevent too many requests on your LMS server
refresh_rate = 5
player_name = MacPlay
min_display_time = 10
# always in the display loop when active
max_priority = 0
# number of seconds to switch priority from max_priority to max_priority-1 when paused
idle_timeout = 20
```

