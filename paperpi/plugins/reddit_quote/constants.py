# relative paths are difficult to sort out -- this makes it easier
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.1.0'
name = 'reddit_quote'
data = {
}

required_config_options = {
    'max_length': 144,
    'max_retries': 10,
}

images = dir_path+'./images/'
tag_image = images+'rabbitsq.png'

quotes_base_url = 'https://www.reddit.com/r/quotes/top/.json?t=week&limit='
quotes_limit = 100
headers = {'User-agent': 'Chrome'}

quotes_url = f'{quotes_base_url}{quotes_limit}'

quote_data_addr = 'data.children'
quote_title_addr = 'data.title'

json_file = f'{name}.json'
# maximum age in seconds (60*60*24 = 86400)
json_max_age = 86400

# see https://english.stackexchange.com/a/59320/441102
attribution_char = '―'

error_text = '"Could not fetch quotes from reddit. Please see the logs." - The Developers'

sample_config = '''
[Plugin: Reddit Quotes]
layout = layout
plugin = reddit_quote
refresh_rate = 100
min_display_time = 50
max_priority = 2
# maximum length of quote (in characters) including spaces, a la Twitter
max_length = 144
'''

