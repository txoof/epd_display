#!/usr/bin/env python3
# coding: utf-8






# your function must import layout and constants
# this is structured to work both in Jupyter notebook and from the command line
try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants
    
from pathlib import Path
from os import path
import json
from time import time
from datetime import datetime
from random import choice






import logging






import feedparser
import qrcode
import requests
# import numpy as np
# import matplotlib.pyplot as plt
from dictor import dictor
from requests.exceptions import RequestException
from currency_symbols import CurrencySymbols
from pycoingecko import CoinGeckoAPI
import pygal
from pygal.style import Style






logger = logging.getLogger(__name__)






# def _generate_sparkline(data, cache_path='./', ratio=(10, 3), generate_keys=[constants.CG_PRICE_KEY]):
#     '''convert dictionary of list of two-tuples into multiple sparkline graphs
    
#     Args:
#         data(dict): {'key'[[v1, v2], [v1, v2]...], 'key2': [[v1, v2]]}
#         cache_path(string): location to output sparkline images
#         ratio(2 tuple): (height, width) of sparkline image in inches
#         generate_keys(list): list of CoinGeco data keys to use when generating sparkline
        
#     Returns:
#         dict  : {'coingeco key': path to sparkline file}
        
#     Coingeco returns the following keys for a typical coin: prices, market_caps, volumes. 
#     Only 'prices' is used by default.
#     '''
    
    
#     # TO DO: 
#     # - [ ] set figsize -- this should match the block ratio in the layout to ensure proper scaling

    
#     logger.debug(f'sparkline ratio: {ratio}')
    
#     sparklines = {}
    
#     for i, v in enumerate(ratio):
#         ratio[i] = v/100
    
#     logger.debug(f'sparkline ratio: {ratio}')
    
#     for key in data.keys():
#         if key in generate_keys:
#             output_file = Path(cache_path)/f'{key}_sparkline.png'
#             # cull just the 1th value from each pair
#             x = [i[1] for i in data[key]]
#             # calculate the mean for the set
#             mean = np.mean(x)

#             # plot the data
#             fig, ax = plt.subplots(1, 1, figsize=ratio)
# #             fig, ax = plt.subplots(1, 1)
# #             fig, ax = plt.subplots(1, 1, gridspec_kw={'width_ratios': [ratio[0]], 
# #                                                       'height_ratios': [ratio[1]]})            
#             plt.plot(x, color='k', linewidth=1)

#             # add a marker to the last value
#             plt.plot(len(x)-1, x[len(x)-1], color='k', marker='o')

#             # Remove the Y axis
#             for k,v in ax.spines.items():
#                 v.set_visible(False)
#             ax.set_xticks([])
#             ax.set_yticks([])

#             # add the mean value line (blue, width 2, style -.-.-)
#             ax.axhline(y=mean, c='gray', linewidth=2, linestyle='-.')

#             try:
#                 logger.debug(f'writing sparkline to file: {cache_path/output_file}')
#                 plt.savefig(cache_path/output_file, dpi=100)
#                 sparklines[key] = output_file
#             except Exception as e:
#                 logging.error(f'failed to write sparkline file: {output_file}: {e}')
#                 pass
            
# #             plt.show()
#             plt.close()
    
#     return sparklines

#     # Save the resulting bmp file to the images directory
# #     plt.savefig(os.path.join(picdir, key+'spark.png'), dpi=72)
# #     plt.close('all') # Close plot to prevent memory error







# $ apt install libcairo2 -- need to make sure this is installed -- add this to the install scripts
# update install scripts to check for SPI configurtation and stuff too






def _pygal_sparkline(data, cache_path='./', width=1000, height=300, 
                     generate_keys=[constants.CG_PRICE_KEY]):
    
    sparklines = {}
    
    for key in generate_keys:
        output_file = Path(cache_path)/f'{key}_sparkline.png'
        my_data = data.get(key, None)
        if not my_data:
            logger.warning(f'expected key "{key}" not found in data')
            continue
        
        # cull just the price value
        price = [i[1] for i in my_data]
        average = sum(price)/len(price)
        average_line = [average for i in price]
        
        chart = pygal.Line(include_x_axis=False, 
                   show_y_labels=False, 
                   show_dots=False,
                   show_legend=False,
                   width=width, height=height,
                   margin=0,            
                   style=constants.CHART_STYLE)
        chart.add('', price)
#         chart.add('', average_line, stroke_style={'dasharray': '5, 2'})
        chart.add('', average_line)        
        try:
            logger.debug(f'writing sparkline to file: {cache_path/output_file}')
            chart.render_to_png(str(output_file))
            sparklines[key] = output_file
        except OSError as e:
            logger.error(f'failed to write sparkline file: {output_file}: {e}')
            continue

            
    return sparklines
        
#     price = [i[1] for i in r['prices']]






def _fetch_token_data(cg, config, json_file):
    '''fetch token data from coingeco using pycoingecko 
    
    Args:
        cg(obj): pycoingeko object
        config(dict) {'coin': 'name', 'fiat': 'fiat symbol', 'interval': 'daily|hourly', 'days': 14}
        json_file(str): path to json file for storing CG data'''
    
    
    json_file = Path(json_file)
    json_data = None

    try:
        mtime  = time() - path.getmtime(json_file)
        logger.debug(f'age of {json_file}: {mtime}')
    except OSError as e:
        logger.debug(f'no json file found')
        mtime = 2**15
    except json.JSONDecodeError as e:
        logger.info(f'{e}')
        mtime = 2**15    

    # replace the cached data if it is older than CG_JASON_MAX_AGE
    if json_file.exists() and mtime < constants.CG_JSON_MAX_AGE:
        try:
            logger.debug(f'using cached {json_file} data')
            with open(json_file) as jf:
                json_data = json.load(jf)
        except OSError as e:
            logger.warning(f'could not open cached JSON file: {e}')
        except json.JSONDecodeError as e:
            logger.error(f'could not decode JSON file: {e}')
            json_data = None
    else:
        logger.debug('cached data expired, fetching fresh data')
        json_data = None

        
    if not json_data:
        logger.debug('downloading fresh data from coingeko')
        try:
            json_data = cg.get_coin_market_chart_by_id(id=config['coin'], 
                                                        vs_currency=config['fiat'],
                                                        days=config['days'],
                                                        interval=config['interval'])
            
        # CG module raises several different exceptions on failure -- catch them ALL
        except Exception as e:
            logger.error(f'failed to fetch prices from coingeko: {e}')           
            
        logger.info('caching data from coingeko')
        try:
            with open(json_file, 'w')  as jf:
                json.dump(json_data, jf)
        except (OSError, TypeError) as e:
            logger.error(f'failed to cache data: {type(e)} {e}')     
    
    return json_data

    






def _fetch_coin_image(cg, coin, cache='./'):
    '''cache coin image from coingeko
    
    Args:
        cg(obj): pycoingeko object
        coin(str): coin to fetch,
        cache(str): path to cache downloaded image'''
    
    cache = Path(cache)
    coin_file = cache/f'{coin}.png'
    unknown_file = '/'.join([constants.IMAGE_PATH, constants.UNKNOWN_COIN])
    
    logger.debug(f'fetching coin image for coin: {coin}')
    if not coin_file.exists():
        logger.debug('no coin image file found, downloading')
        try:
            response = cg.get_coin_by_id(id=coin, 
                                         localization='false',
                                         tickers=False,
                                         market_data=False,
                                         community_data=False,
                                         developer_data=False,
                                         sparkline=False)
            
        except Exception as e:
            logging.error(f'error fetching data: {type(e)} - {e}')
            response = None
            coin_file = unknown_file
        
        coin_url = dictor(response, 'image.large')
        
        if coin_url:
            try:
                r = requests.get(coin_url)
            except RequestException as e:
                logging.error(f'failed to fetch coin image file: {e}')
                coin_file = unkown_file
            
            if r.status_code == 200:
                with open(coin_file, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                logger.debug(f'wrote coin image file: {coin_file}')
            else:
                coin_file = unknown_file    
    else:
        logger.info(f'using cached image: {coin_file}')
    
    return coin_file






def _format_number(n):
    '''convert number to shortened notation
    
    Args:
        n(int, real): integer or real number
        
    Returns: 
        (str) in the format 1.2k, 82.2M, 9.2B, 199.2T, 6.2e+23'''
    digits = len(str(round(n)))
    if digits < 16:
        if digits in range(0, 4):
            exp = 0
            val = ''
        if digits in range(4, 7):
            exp = 3
            val = 'k'
        if digits in range(7, 10):
            exp = 6
            val = 'M'
        if digits in range(10, 13):
            exp = 9
            val = 'B'
        if digits in range(13, 16):
            exp = 12
            val = 'T'
        return f'{n/10**exp:.1f}{val}'
    else:
        return f'{n:.1e}'






def _fetch_feed_articles(url, cache_path='./'):
    '''return random article from rss feed
    
    Args:
        url(str): url for rss feed
        cache_path: location to cache downloaded rss'''
    article_list = []
    default_article = {'title': f'Error fetching feed: {url}',
                       'link': None}

    json_file = Path(cache_path)/constants.FEED_JSON
    
    logger.debug(f'fetching feeds from {url}')
    
    logger.debug(f'checking age of cached feed data')
    try:
        mtime  = time() - path.getmtime(json_file)
        logger.debug(f'age of {json_file}: {mtime}')
    except OSError as e:
        logger.debug(f'no json file found')
        mtime = 2**15
    except json.JSONDecodeError as e:
        logger.info(f'{e}')
        mtime = 2**15    
    
    # replace the cached data if it is older than CG_JASON_MAX_AGE
    if json_file.exists() and mtime < constants.FEED_JSON_MAX_AGE:
        try:
            logger.debug(f'using cached {json_file} data')
            with open(json_file) as jf:
                json_data = json.load(jf)
        except OSError as e:
            logger.warning(f'could not open cached JSON file: {e}')
        except json.JSONDecodeError as e:
            logger.error(f'could not decode JSON file: {e}')
            json_data = None
    else:
        logger.debug('cached data expired, fetching fresh data')
        json_data = None

        
    if not json_data:
        logger.debug(f'downloading fresh feed data from {url}')
        json_data = feedparser.parse(url)
    
    
    if json_data.get('bozo', 2**15) > 0:
        logger.error(f'failed to fetch RSS feed at {url}: {json_data.get("bozo_exception", "UNKNOWN ERROR")} ')
    else:
        logger.info('caching data from feed')
        try:
            with open(json_file, 'w')  as jf:
                json.dump(json_data, jf)
        except (OSError, TypeError) as e:
            logger.error(f'failed to cache data: {type(e)} {e}')     
        

    
    
    for entry in json_data.get('entries'):
        article_list.append({'title': entry.get('title'),
                             'link': entry.get('link')})
        
    
    if len(article_list)< 1:
        article_list.append(default_article)
    
    return choice(article_list)
        
    
    
    
    






# make sure this function can accept *args and **kwargs even if you don't intend to use them
def update_function(self, *args, **kwargs):
    '''update function for crypto plugin provides: value of crypto token versus fiat currency
    along with sparkline, volume and 24 hour change as well as rss feed and qr code
    for related article (if available)
    
    During each update the current price is pulled from CoinGecko. Each hour the sparkline
    data is updated.
    
    This plugin can be specified multiple times in the configuration file
    to display multiple currencies:
    
    [Plugin: Crypto Bitcoin v USD]
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
    
    [Plugin: Crypto Dogecoin v GBP]
    layout = layout
    # fiat currency to use for comparison
    fiat = gbp
    # crypto currency to track
    coin = dogecoin
    # days of data to display
    days = 14
    # interval to show on sparkline
    interval = hourly
    # rss news feed to display
    rss_feed = https://bitcoinmagazine.com/.rss/full/
    
    
    Configuration Requirements:
        self.config(`dict`):
                'fiat': ticker value for national currencey, e.g. usd, jpy, gbp
                'coin': CoinGecko ticker value for crypto token
                'days': number of days of historical value to pull
                'interval': interval for sparkline ('hourly' or 'daily')
                'rss_feed': RSS feed to display
                
    Args:
        self(namespace): namespace from plugin object
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))
    %U'''   
  
    general_failure = False
    is_updated = False
    data = {}
    priority = 2**15
    config = self.config
    
    #CoinGeko API object
    cg = CoinGeckoAPI()
    cg.request_timeout = constants.CG_TIMEOUT
    
    cache_dir = Path(self.cache.path)/f"{self.name}_{config['coin']}_v_{config['fiat']}"
    if not cache_dir.exists():
        logger.debug(f'making cache directory: {cache_dir}')
        cache_dir.mkdir()
    
    json_file = cache_dir/constants.CG_PRICES_JSON
        
    
    # set required values if they aren't specified
    for k, v in constants.REQUIRED_CONFIG_OPTIONS.items():
        config[k] = config.get(k, v)
        # set type to match type in constants
        try:
            config[k] = type(v)(config[k])
        except ValueError as e:
            logger.warning(f'bad value in config file "{k}": {config[k]}; falling back to default value "{v}"')
            config[k] = v
            
            
    logger.debug(f'updating {self.name} for {self.config["coin"]}:{self.config["fiat"]}')  
    
    # set width, height for sparkline image
    for i, key in enumerate(['width', 'height']):
        try:
            config['spark_ratio'][i] = self.layout['sparkline'][key] * self.resolution[i]
        except KeyError as e:
            logger.error('layout does not contain a properly formatted key for `sparkline`')
            general_failure = True

    # get the latest token data
    json_data = _fetch_token_data(cg, config, json_file)

    if json_data:
#         sparklines = _generate_sparkline(json_data, cache_dir, ratio=config['spark_ratio'])
        sparklines = _pygal_sparkline(json_data, cache_dir, width=config['spark_ratio'][0], height=config['spark_ratio'][1])
    else:
        general_failure = True
        logger.error('no JSON data returned. see previous errors')

    # get the current price right now
    try:
        current_price = cg.get_price(ids=config['coin'], vs_currencies=config['fiat'], 
                                     include_24hr_vol=True,
                                     include_24hr_change=True)
    except Exception as e:
        logging.error(f'failed to get current price: {e}')
        current_price = None

    logger.debug(f'CURRENT PRICE: {current_price}')
    if current_price:
        # simplify the dict
        current_price = current_price[config['coin']]
        try:
            values = {'coin_price': current_price[config['fiat']],
                      'change': current_price[f'{config["fiat"]}_24h_change'],
                      'volume': current_price[f'{config["fiat"]}_24h_vol']}
        except KeyError as e:
            logger.error(f'error setting current values: {type(e)} - {e}')
            general_failure = True
    else:
        logger.error(f'failed to fetch current value from coingeko')
        general_failure = True

    rss_data = _fetch_feed_articles(config['rss_feed'], cache_dir)
    rss_qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=3,
                           border=1,)
    logger.debug(f'creating qr code with data: {rss_data["link"]}')
    rss_qr.add_data(rss_data['link'])
    qr_file = cache_dir/constants.QR_FILE
    rss_qr.make_image().save(qr_file)
        
    if not general_failure:
        
        # format coin price
        cp = values ['coin_price']
        if cp > 1000:
            cp = _format_number(cp)
        else:
            cp = round(cp, 4)
            
        values['coin_price'] = cp
            
        
        # format change 
        if abs(values['change']) > 1:
            c = round(values['change'])
        else:
            c = round(values['change'], 2)
            
        # add '+' for positive values
        if c > 0:
            c = f'+{c}'
        values['change'] = c
        

        # convert to a value string e.g. 12.3B
        values['volume'] = _format_number(values.get('volume', 0))
        
        # Generate strings
        time_string = datetime.strftime( datetime.now(), '%H:%M %a %d %b, %Y')
        update_time = f'Updated: {time_string}. {config["days"]} day data'
        coin_file = _fetch_coin_image(cg, config['coin'], cache_dir)

        try:
            symbol = CurrencySymbols.get_symbol(config["fiat"].upper())
        except TypeError as e:
            logger.error(f'could not find currency: {type(e)} - {e}')
            symbol = '?'
        finally:
            if not symbol:
                symbol = '?'

        price_string = f'{symbol}{values["coin_price"]}'
        change_vol_string = f'{values["change"]}% vol:{symbol}{values["volume"]}'
        

        try
            data = {
                'update_time': update_time,
                'coin_file': coin_file,
                'price_string': price_string,
                'change_vol_string': change_vol_string,
                'sparkline': sparklines['prices'],
                'rss_feed': rss_data['title'],
                'qr_code': qr_file
            }
            is_updated = True            
        except KeyError as e:
            logger.error(f'KeyError: {e}')
            data = {}
            is_updated = False
            
        priority = self.max_priority
    else:
        logging.error('general failure - see errors above')
                
    return (is_updated, data, priority)






# from library.CacheFiles import CacheFiles
# from library.SelfDummy import SelfDummy
# s = SelfDummy()
# s.cache = CacheFiles()

# s.cache

# config = {
#     'coin': 'bitcoin',
#     'fiat': 'usd',
#     'days': '365',
#     'interval': 'hourly'
# }
# # config = {}
# s.max_priority = 1
# s.config = config
# s.name = 'crypto'
# s.layout = {'sparkline': {
#         'type': 'ImageBlock',
#         'image': True,
#         'width': .4,
#         'height': .25,
#         'abs_coordinates': (None, None),
#         'relative': (),
#         },
#       }
# s.resolution = (1200, 800)
    

# a = update_function(s)
# a










# logging.basicConfig(level=logging.DEBUG)
# logger.setLevel('WARNING')
# logging.root.setLevel('WARNING')






# from library.CacheFiles import CacheFiles
# from library.Plugin import Plugin
# test_plugin = 0
# def test_plugin():
#     '''This code snip is useful for testing a plugin from within Jupyter Notebook'''
#     from library import Plugin
#     from IPython.display import display
#     # this is set by PaperPi based on the configured screen
#     test_plugin = Plugin(resolution=(1200, 825))
#     # this is pulled from the configuration file; the appropriate section is passed
#     # to this plugin by PaperPi during initial configuration
#     test_plugin.config = {
#     'coin': 'bitcoin',
#     'fiat': 'usd',
#     'days': '14',
#     'interval': 'hourly'
# }
# #     test_plugin.layout = layout.layout
#     test_plugin.layout = layout.ticker_hd
#     # this is done automatically by PaperPi when loading the plugin
#     test_plugin.cache = CacheFiles()
#     test_plugin.update_function = update_function
#     test_plugin.update()
#     display(test_plugin.image)
#     return test_plugin
# my_plugin = test_plugin
# my_plugin()


