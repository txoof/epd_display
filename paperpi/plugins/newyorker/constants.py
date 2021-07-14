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

private_cache = 'newyorker'