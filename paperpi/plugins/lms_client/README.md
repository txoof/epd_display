# lms_client
![sample image for plugin lms_client](./lms_client_sample.png)
```
 
error importing plugins.lms_client.lms_client: No module named 'plugins'
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

