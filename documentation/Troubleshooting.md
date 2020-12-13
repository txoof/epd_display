## Troubleshooting
### **Issue:** Streaks, and poor quality text
    - <img src=./images/trouble_streaks.jpg alt="streaks" width=500 />
    - <img src=./images/trouble_bad_text.jpg alt="bad text" width=500 />
**Possible Solution:** 

- Use JST connector instead of plugging the waveshare HAT directly into the raspberry pi (see table below)
    - try switching to the wire JST connector and plug the black dupont connectors directly into the GPIO headers of the PI (see table below)
    - See [pinout.xyz](https://pinout.xyz) for help locating the proper GPIO pins

### **Issue:** PaperPi does not appear to start on boot when run as a daemon

**Possible Solution:** 

- Wait for the first plugin to expire (check the `min_display_time` setting in `paperpi.ini`). This is a [known issue](https://github.com/txoof/epd_display/issues/1#issue-765246248) when running PaperPi in daemon mode.
- Check `/var/log/daemon.log` for details -- PaperPi publishes all logging output here
    - `$ tail -f /var/log/daemon.log`

#### JST Connector Pinout

| HAT JST Pin | Pi Pin Name       | Physical Pin Number |
|-------------|-------------------|---------------------|
| 3.3V        | 3.3V              | 1                   |
| GND         | GND               | 3                   |
| DIN         | MOSI              | 19                  |
| CLK         | SCLK              | 23                  |
| CS          | CE0               | 24                  |
| DC          | GPOIO 25(BCM)     | 22                  |
| RST         | GPIO 17(BCM)      | 11                  |
| BUSY        | GPIO 24(BCM)      | 18                  |



