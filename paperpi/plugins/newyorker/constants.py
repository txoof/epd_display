import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.0.1'
name = 'New Yorker Cartoon'


data = { 
  'comic': 'img',
  'text': 'str',
  'time': 'str',
}

feed_url = 'https://www.newyorker.com/feed/cartoons/daily-cartoon'

images_path = dir_path + '/./images/'

private_cache = f'{name}/'

expire_cache = 10

sample_config = '''
[Plugin: New Yorker Comic]
layout = layout
plugin = newyorker
# number of past days to choose from
day_range = 5
refresh_rate = 120
min_display_time = 60
max_priority = 2
'''
