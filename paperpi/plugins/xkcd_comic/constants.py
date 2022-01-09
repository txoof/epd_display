# relative paths are difficult to sort out -- this makes it easier
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.1.0'
name = 'xkcd_comic'
data = {
    'image_file': 'path to downloaded comic image',
    'alt': 'alt text for comic',
    'num': 'number of comic',
    'safe_title': 'printable title'
}

default_comic = '1495'

required_config = {
    'max_x': 800,
    'max_y': 600,
    'max_retries': 10,
    'resize': 0,
}

sample_config = '''
[Plugin: XKCD Comic Plugin]
# default layout
layout = layout
plugin = xkcd_comic
refresh_rate = 1200
min_display_time = 120
# maximum x dimension of comic image
max_x = 800
# maximum y dimension of comic image
max_y = 600
# max attempts to find a suitable comic image
# 0 do not rsize small comics / 1 maximize small comics to max_x, max_y
resize = 0
max_retries = 10
max_priority = 2
'''

image_path = f'{name}/'

xkcd_url = 'https://xkcd.com/'
xkcd_json_doc = 'info.0.json'
