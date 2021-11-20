from pathlib import Path


app_name = 'PaperPi'
contact = 'aaron.ciuffo@gmail.com'
devel_name = f'com.txoof.{app_name.lower()}'
version = '0.2.13.0'
#version = __version__
url = 'https://github.com/ txoof/epd_display'

## Runtime Constants

absolute_path = Path(__file__).resolve().parent

## configuration

# configuration file directory
# config_path = Path('./config')
config_path = Path('./config')

# default name for configuration file
config_filename = f'{app_name.lower()}.ini'
#config_base = Path(config_path/config_filename).resolve()
config_base = config_path/config_filename

# path for user config file
config_user = Path(f'~/.config/{devel_name}/{config_filename}').expanduser().resolve()

# path for system configurationf ile
#config_system = Path(f'/etc/default/{config_filename}').resolve()
config_system = Path(f'/etc/default/{config_filename}')

# path to logging configuration file
#logging_config = Path(config_path/'./logging.cfg').resolve()
logging_config = f'{config_path}/logging.cfg'



# Plugins Information
# plugin base directory
plugins = 'plugins'

## WaveShare Information
ws_version = '337fa63 2021-06-22 20:12:03 +0800'

# local version of waveshare library
waveshare_epd = 'waveshare_epd'



version_string = f'''
{app_name}
Version: {version}
{url}
'''

