# LibreSpot_Client
sample data:
 ```
(True, {'title': 'Postcards From Hell', 'artist': 'The Wood Brothers', 'album': 'Loaded', 'artwork_url': 'https://i.scdn.co/image/ab67616d0000b273f67da3f6371b67731d2459b9', 'duration': 284862, 'player': 'SpoCon-Spotify', 'mode': 'play', 'id': '72i7dwVrHdfDnr3qmINh5U', 'coverart': PosixPath('/tmp/1e2q8_c8/72i7dwVrHdfDnr3qmINh5U')}, -1)
```
![LibreSpot_Client](./Documentation/images/LibreSpot_Client.png)
Layout:
```
{'coverart': {'image': True, 'max_lines': None, 'padding': 5, 'width': 0.3333333333333333, 'height': 0.6, 'abs_coordinates': (0, 0), 'hcenter': True, 'vcenter': True, 'relative': False}, 'title': {'image': None, 'max_lines': 3, 'padding': 4, 'width': 0.6666666666666666, 'height': 0.6, 'abs_coordinates': (None, 0), 'relative': ['coverart', 'title'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/librespot_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}, 'artist': {'image': None, 'max_lines': 2, 'padding': 4, 'width': 1, 'height': 0.2, 'abs_coordinates': (0, None), 'relative': ['artist', 'title'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/librespot_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}, 'album': {'image': None, 'max_lines': 2, 'padding': 4, 'width': 1, 'height': 0.2, 'abs_coordinates': (0, None), 'relative': ['album', 'artist'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/librespot_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}}
```
