version = '0.1.2'
name = 'lms_client'
#  path for private cache with the temp directory
private_cache = f'{name}/'
# days worth of album images to retain in cache
expire_cache = 3

data = {
        'id': 0,
        'title': 'Err: No Player',
        'artist': 'Err: No Player',
        'coverid': 'Err: No Player',
        'duration': 0,
        'album_id': 'Err: No Player',
        'genre': 'Err: No Player',
        'album': 'Err: No Player',
        'artwork_url': 'Err: No Player',
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
