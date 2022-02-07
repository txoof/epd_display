import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.1.0'
name = 'home_assistant'

#  path for private cache with the temp directory
private_cache = f'{name}/'
# days worth of album images to retain in cache
expire_cache = 3

img_file = dir_path+'/player.png'

sample_config = '''
[Plugin: Home Assistant]
layout = layout
plugin = home_assistant
min_display_time = 30
max_priority = 1
home_assistant_basepath = https://IP:8123
# home assistant access token
home_assistant_token = 
# all four sensors are mandatory to add
entity1_name = Friendly name (ex Indoor)
entity1_id = home assistant sensor id
entity2_name = Friendly name (ex Outdoor)
entity2_id = home assistant sensor id
entity3_name = Friendly name (ex Outdoor)
entity3_id = home assistant sensor id
entity4_name = Friendly name (ex Outdoor)
entity5_id = home assistant sensor id
media_id = media player id
'''
