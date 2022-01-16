# relative paths are difficult to sort out -- this makes it easier
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

version = '0.1.0'
name = 'crypto'
data = {}

REQUIRED_CONFIG_OPTIONS = {
    'fiat': 'usd',
    'coin': 'bitcoin',
    'days': 14,
    'interval': 'hourly',
    'spark_ratio': [10, 3],
    'rss_feed': 'https://bitcoinmagazine.com/.rss/full/'
}

#time out in seconds
CG_TIMEOUT = 15
CG_PRICES_JSON = 'all_prices.json'
# maximum age in seconds 60 sec * 59 minutes
CG_JSON_MAX_AGE = 60*59
CG_PRICE_KEY = 'prices'

IMAGE_PATH = dir_path+'/images/'
UNKNOWN_COIN = 'unknown.png'

FEED_JSON = 'feed.json'
# maximum age in seconds -- 2 hours
FEED_JSON_MAX_AGE = 60*60*2

QR_FILE = 'qr.png'

sample_config = '''
[Plugin: Crypto Bitcoin v USD]
plugin = crypto
layout = layout
# fiat currency to use for comparison
fiat = usd
# crypto currency to track
coin = bitcoin
# days of data to display
days = 14
# interval to show on sparkline
interval = hourly
# rss news feed to display
rss_feed = https://bitcoinmagazine.com/.rss/full/
min_display_time = 30
# refresh data every 5 minutes
refresh_rate = 300
max_priority = 2
'''

