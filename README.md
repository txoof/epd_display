# PaperPi
|     |     |
|:---:|:---:|
|<img src=./paperpi/plugins/splash_screen/splash_screen.layout-sample.png alt="Splash Screen" width=400/> Splash Screen| <img src=./documentation/images/PaperPi_Demo_frame.gif alt="PaperPi" width=400 /> PaperPi Weather Plugin|

PaperPi is an e-Paper display with multiple rotating display plugins that contain dynamic content.

PaperPi is a quiet and clean portal to the internet. No loud colors, no busy animations, just a lovely selection of the information you want without buzz and distraction. PaperPi rotates through your choice of plugin screens at the pace you choose. 


PaperPi is written to work with almost all of the [WaveShare](https://www.waveshare.com/product/displays/e-paper.htm) SPI displays out of the box. PaperPi will work with the tiny 2" displays all the way up to the 10" HD displays with minimal configuration. Check the complete list of [supported screens](#supportedScreens)


For information on building a frame, case and custom cable, see [these instructions](./documentation/Frame_Cable_Case.md).

To get started, jump to the **[Setup Instructions](#setup)**


## Plugins
PaperPi supports many different plugins and layouts for each plugin.

 
### [Complete Plugins List](./documentation/Plugins.md)

| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img src=./paperpi/plugins/librespot_client/librespot_client.layout-sample.png alt="librespot plugin" width=300 />[LibreSpot (spotify) Plugin](./paperpi/plugins/librespot_client/README.md)|<img src=./paperpi/plugins/word_clock/word_clock.layout-sample.png alt="word clock plugin" width=300 />[Word Clock](./paperpi/plugins/word_clock/README.md)|<img src=./paperpi/plugins/lms_client/lms_client.layout-sample.png alt="lms client plugin" width=300 />[Logitech Media Server Plugin](./paperpi/plugins/lms_client/README.md)|
|<img src=./paperpi/plugins/moon_phase/moon_phase.layout-sample.png alt="decimal binary clock" width=300 />[Moon Phase](./paperpi/plugins/moon_phase/README.md)|<img src=./paperpi/plugins/met_no/met_no.layout-sample.png alt="met_no plugin" width=300 />[Met.no Weather](./paperpi/plugins/met_no/README.md)|<img src=./paperpi/plugins/crypto/crypto.layout-sample.png alt="Crypto Currency Ticker" width=300 />[Crypto Currency](./paperpi/plugins/crypto/README.md)|
|<img src=./paperpi/plugins/reddit_quote/reddit_quote.layout-sample.png alt="reddit/r/quotes" width=300 />[Reddit Quotes](./paperpi/plugins/reddit_quote/README.md)|<img src=./paperpi/plugins/xkcd_comic/xkcd_comic.layout-sample.png alt="XKCD Comic" width=300 />[XKCD Comic](./paperpi/plugins/xkcd_comic/README.md)|<img src=./paperpi/plugins/basic_clock/basic_clock.layout-sample.png alt="Basic Clock" width=300 />[Basic Clock](./paperpi/plugins/basic_clock/README.md)| |


## Changes
See the [Change Log](./documentation/Change_Log.md) for a complete list of updates

<a name="requirements"></a>
## Requirements

### Required Hardware

* Raspberry Pi (Pi 4, Pi 3, and Pi Zero)
* Raspberry Pi OS Buster or later (64-bit supported)
* [WaveShare EPD Screen](https://www.waveshare.com/product/displays/e-paper.htm) with PiHat
  * see the full list of currently [supported screens](#supportedScreens)
  * Note: HDMI screens are not supported
     
### Optional Hardware

* [HiFiBerry hat](https://www.hifiberry.com/shop/#boards) (*optional*) 
    * The HiFiBerry DAC+ PRO and similar boards add high-quality audio output to the Pi so it can act as a display and also work as a LMS client player using squeezelite
    * GPIO 2x20 headers **must be added** to the HiFiBerry HAT to provide an interface for the WaveShare HAT.
    * HiFiBerry's [DAC+ Bundle](https://www.hifiberry.com/shop/bundles/hifiberry-dac-bundle-4/) with the following configuraiton is a good choice:
        * DAC+ Pro 
        * Acrylic Case for (RCA) AND DIGI+
        * Raspberry Pi 4B 2GB (1GB should be sufficient as well)
        * 16GB SD Card
        * PowerSupply (USB C 5.1V/3A)
        * 2x20 Pin Male Header (required for WaveShare HAT)

### Optional Software
PaperPi plugins work with a variety of other software such as Logitech Media Server and Spotify. Check the [Plugin documentation](./documentation/Plugins.md) for further instructions

<a name="setup"> </a>
## Setup
PaperPi requires only small amount of setup. 

### Hardware/OS Setup
**All Waveshare Screens**

The WaveShare displays require the SPI interface. SPI can be enabled through the `raspi-config` command.
1. Enable SPI (see images below)
    - `$ sudo raspi-config` > Interface Options > SPI > Yes
2. Reboot
    - `$ sudo shutdown -r now`
    
| |
|:-------------------------:|
|<img src=./documentation/images/raspi_config_00_iface_opts.png alt="librespot plugin" width=500 />|
|<img src=./documentation/images/raspi_config_01_spi.png alt="librespot plugin" width=500 />|
|<img src=./documentation/images/raspi_config_02_spi_enabled.png alt="librespot plugin" width=500 />|


### Userland Setup
PaperPi can be run directly on-demand from a user account such as the default "pi" user. Any other user will work as well, but the user must be a member of the spi group.
1. [Download the tarball](https://github.com/txoof/epd_display/raw/master/paperpi_latest.tgz)
    - `$ wget https://github.com/txoof/epd_display/raw/master/paperpi_latest.tgz`
2. Decompress the archive: `tar xvzf paperpi.tgz`
3. Launch PaperPi: `$ ./paperpi/dist/paperpi`
    - On the first run PaperPi will create a configuration file in `~/.config/com.txoof.paperpi/paperpi.ini` and then exit
4. Edit the configuration file to match your needs. The default configuration will provide a reasonable starting point
    - `$ nano ~/.config/com.txoof.paperpi/paperpi.ini`
        - At minimum you must specify the `display_type`
        - If you are using an HD IT8951 display, you must also set the `vcom` value which can be found on the ribon cable.
        ```
        # choose the display type that matches your e-paper pannel 
        display_type = epd2in7
        # vcom value for HDIT8951 displays
        vcom = 0.0
        ```
        - See the list of [supported screens](#supportedScreens) for more information
5. Launch PaperPi again -- you should immediately see a splash screen followed shortly by the first active plugin.
6. Press `ctrl+c` to shutdown paperpi cleanly
    - Waveshare recommends clearing pannels to a blank state prior to long-term storage

### Daemon Setup
PaperPi is designed to run as an unattended daemon process that starts at system boot.

1. [Download the tarball](https://github.com/txoof/epd_display/raw/master/paperpi_latest.tgz)
    - `$ wget https://github.com/txoof/epd_display/raw/master/paperpi_latest.tgz`
2. Decompress the archive: `tar xvzf paperpi.tgz`
3. Install PaperPi as a service, run the install script: `$ sudo ./install.sh` 
    - This will:
        * add the necessary service users and groups
        * add a configuration file to `/etc/defaults/paperpi.ini`
        * install PaperPi as a systemd service
4. Edit `/etc/defaults/paperpi.ini` to configure a `display_type` and enable any plugins
    - `$ sudo nano /etc/defaults/paperpi.ini`
    - At minimum you must specify the `display_type`
    - See the list of [supported screens](#supportedScreens) for more information
5. Start PaperPi: `$ sudo systemctl restart paperpi` 
    - PaperPi will now start and restart at boot as a systemd service
    - PaperPi may fail to clear the screen when the daemon is stopped. This a known [issue](https://github.com/txoof/epd_display/issues/19).


## Developing PaperPi
If you would like to develop [plugins](./documentation/Plugins.md) for PaperPi, you will likely need a working build environment. 

### Requirements:
* python 3.7+
* pipenv

**Create a Build Environment**

1. Clone the repo: `https://github.com/txoof/epd_display.git`
2. Run `$ create_devel_venv.sh` to create a build environment
    - This will check for all necessary libraries and python modules
3. The build script will then attempt to build a binary of PaperPi using pyintsaller 
    - executables are stored in `./dist/`
    
**Build Paperpi**

1. Create a build environment (see above)
2. Run `$ build.sh` to create a pyinstaller one-file distributable
3. If you've updated documentation in any plugins, be sure to rebuild the documentation with `$ pipenv run python3 create_docs.py`
4. Submit a PR if you'd like your changes included in the official distribution

## Contributing
PaperPi's core is written and maintained in Jupyter Notebook. If you'd like to contribute, please make pull requests in the Jupyter notebooks. Making PRs to the `.py` files means manually moving the changes into the Jupyter Notebook and adds considerable work to the build/test process.

Plugins can be pure python, but should follow the [guide provided](./documentation/Plugins.md).

See [this gist](https://gist.github.com/txoof/ed4319db317f813b9e500ff190ca4a87) for a quick guide for setting up a jupyter environment on a Raspberry Pi.

<a name="supportedScreens"> </a>
## Supported Screens
Most NON-IT8951 screens are only supported in 1 bit (black and white) mode. Color output is not supported at this time. Some waveshare drivers do not provide 'standard' `display` and `Clear` methods; these displays are not supported at this time.

All IT8951 Screens now support 8 bit grayscale output.

Some WaveShare screens that support color output will also work with with the non-colored driver. Using the 1 bit driver can yield significantly better update speeds. For example: the `epd2in7b` screen takes around 15 seconds to update even when refreshing a 1 bit image, but can be run using the `epd2in7` module in 1-bit mode which takes less than 2 seconds to update.

**WaveShare Screen**

NN. Board        Supported:
--  -----        ----------
00. epd1in02     supported: False
 * AttributeError: module does not support `EPD.display()`
01. epd1in54     supported: True
02. epd1in54_V2  supported: True
03. epd1in54b    supported: True
04. epd1in54b_V2 supported: True
05. epd1in54c    supported: True
06. epd2in13     supported: True
07. epd2in13_V2  supported: True
08. epd2in13b_V3 supported: True
09. epd2in13bc   supported: True
10. epd2in13d    supported: True
11. epd2in66     supported: True
12. epd2in66b    supported: True
13. epd2in7      supported: True
14. epd2in7b     supported: True
15. epd2in7b_V2  supported: True
16. epd2in9      supported: True
17. epd2in9_V2   supported: True
18. epd2in9b_V3  supported: True
19. epd2in9bc    supported: True
20. epd2in9d     supported: True
21. epd3in7      supported: False
 * unsupported `EPD.Clear()` function
 * AttributeError: module does not support `EPD.display()`
22. epd4in01f    supported: True
23. epd4in2      supported: True
24. epd4in2b_V2  supported: True
25. epd4in2bc    supported: True
26. epd5in65f    supported: True
27. epd5in83     supported: True
28. epd5in83_V2  supported: True
29. epd5in83b_V2 supported: True
30. epd5in83bc   supported: True
31. epd7in5      supported: True
32. epd7in5_HD   supported: True
33. epd7in5_V2   supported: True
34. epd7in5b_HD  supported: True
35. epd7in5b_V2  supported: True
36. epd7in5bc    supported: True
37. All IT8951 Based Panels

<a name="knownIssues"> </a>
## Isuses
Please [open tickets at GitHub](https://github.com/txoof/epd_display/issues).



