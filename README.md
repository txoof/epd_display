# PaperPi
![lms_client plugin](./paperpi/plugins/splash_screen/splash_screen_sample.png)

E-Paper display with multiple display plugins. 

PaperPi is designed run as a daemon process to display a vairety of plugins to SPI based e-paper/e-ink displays with long refresh delays. It has been specifically written to work with the [WaveShare](https://www.waveshare.com/product/displays/e-paper.htm) SPI displays.

PaperPi rotates through a user-configured selection of plugins each represented by a single static "screen." After the plugin screen has "expired", the next plugin with the highest priority (lowest value) will be displayed, eventually cycling through all the plugins. 


## Plugins
PaperPi supports many different plugins and layouts for each plugin. The plugin structure is open and documented to allow building your own plugins or customizing existing plugins.
 
[Complete Plugins  List](./documentation/Plugins.md)

| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img src=./paperpi/plugins/librespot_client/librespot_client_sample.png alt="librespot plugin" width=300 />[LibreSpot (spotify) Plugin](./paperpi/plugins/librespot_client/README.md)|<img src=./paperpi/plugins/word_clock/word_clock_sample.png alt="word clock plugin" width=300 />[Word Clock](./paperpi/plugins/word_clock/README.md)|<img src=./paperpi/plugins/lms_client/lms_client_sample.png alt="lms client plugin" width=300 />[Logitech Media Server Plugin](./paperpi/plugins/lms_client/README.md)|
|<img src=./paperpi/plugins/dec_binary_clock/dec_binary_clock_sample.png alt="decimal binary clock" width=300 />[Decimal-Binary Clock](./paperpi/plugins/dec_binary_clock/README.md)|<img src=./paperpi/plugins/met_no/met_no_sample.png alt="met_no plugin" width=300 />[Met.no Weather](./paperpi/plugins/met_no/README.md)|<img src=./paperpi/plugins/pi_dash/pi_dash_sample.png alt="Pi Dashboard" width=300 />[Pi Dashboard](./paperpi/plugins/pi_dash/README.md)|

<a name="requirements"></a>
## Requirements

### Required Hardware
* Raspberry Pi 4B
    - A Pi3 and possibly a Pi Zero are likely sufficient, but are untested at this time (Nov 2020)
* [WaveShare EPD SPI-only Screen](https://www.waveshare.com/product/displays/e-paper.htm) with PiHat
    - UART, SPI/USB/I80 screens are **not supported** as there is no python library for diving these boards
     
### Optional Hardware
* [HiFiBerry hat](https://www.hifiberry.com/shop/#boards) (*optional*) 
    * The HiFiBerry DAC+ PRO and similar boards add high-quality audio output to the Pi so it can act as a display and also work as a LMS client player using squeezelite
    * GPIO 2x20 headers **must be added** to the board to support WaveShare HAT
    * HiFiBerry's [DAC+ Bundle](https://www.hifiberry.com/shop/bundles/hifiberry-dac-bundle-4/) with the following configuraiton is a good choice:
        * DAC+ Pro 
        * Acrylic Case for (RCA) AND DIGI+
        * Raspberry Pi 4B 2GB (1GB should be sufficient as well)
        * 16GB SD Card
        * PowerSupply (USB C 5.1V/3A)
        * 2x20 Pin Male Header (required for WaveShare HAT)

### Optional Software

## Quick Install





```python
./paperpi/plugins/splash_screen/README.md
```


```python
!jupyter-nbconvert --to markdown README.ipynb
```

    [NbConvertApp] Converting notebook README.ipynb to markdown
    [NbConvertApp] Writing 0 bytes to README.md

