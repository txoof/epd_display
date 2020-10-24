# Logitech_Media_Server_Client
sample data:
 ```
(True, {'id': 10380, 'title': 'Young Rabbits', 'artist': 'The Jazz Crusaders', 'coverid': '276a2509', 'duration': 469.626, 'album_id': '1289', 'genre': 'Jazz', 'album': 'The Festival Album', 'artwork_url': 'http://192.168.178.9:9000/music/276a2509/cover.jpg', 'mode': 'play', 'coverart': PosixPath('/tmp/kchyni5n/1289')}, -1)
```
![Logitech_Media_Server_Client](./Documentation/images/Logitech_Media_Server_Client.png)
Layout:
```
{'coverart': {'image': True, 'max_lines': None, 'padding': 5, 'width': 0.3333333333333333, 'height': 0.6, 'abs_coordinates': (0, 0), 'hcenter': True, 'vcenter': True, 'relative': False}, 'title': {'image': None, 'max_lines': 3, 'padding': 4, 'width': 0.6666666666666666, 'height': 0.6, 'abs_coordinates': (None, 0), 'relative': ['coverart', 'title'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/lms_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}, 'artist': {'image': None, 'max_lines': 2, 'padding': 4, 'width': 1, 'height': 0.2, 'abs_coordinates': (0, None), 'relative': ['artist', 'title'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/lms_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}, 'album': {'image': None, 'max_lines': 2, 'padding': 4, 'width': 1, 'height': 0.2, 'abs_coordinates': (0, None), 'relative': ['album', 'artist'], 'hcenter': True, 'vcenter': True, 'font': '/home/pi/src/epd_display/paperpi/plugins/lms_client/../../fonts/Open_Sans/OpenSans-Regular.ttf'}}
```
