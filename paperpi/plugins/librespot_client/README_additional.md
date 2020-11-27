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