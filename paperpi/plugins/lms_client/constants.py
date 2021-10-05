version = '0.1.2'
name = 'lms_client'
#  path for private cache with the temp directory
private_cache = f'{name}/'
# days worth of album images to retain in cache
expire_cache = 3

data = {
        'id': 0,
        'title': 'No Player',
        'artist': 'No Player',
        'coverid': 'No Player',
        'duration': 0,
        'album_id': 'No Player',
        'genre': 'No Player',
        'album': 'No Player',
        'artwork_url': 'No Player',
        'coverart': 'None',
        'mode': 'None'
    }
sample_config = '''
[Plugin: LMS - Your Player Name]
layout = layout
plugin = lms_client
player_name = Your Player Name
refresh_rate = 5
min_display_time = 30
max_priority = 0
idle_timeout = 15
'''
