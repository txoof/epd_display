from pathlib import Path

app_name = 'PaperPi'
devel_name = f'com.txoof.{app_name.lower()}'
version = '0.0.1'
url = 'https://github.com/txoof/epd_display'

## configuration
required_config = {
                   'display_type': None,
}

config_filename = f'{app_name.lower()}.ini'
config_base = Path(config_filename).resolve()
config_user = Path(f'~/{devel_name}/{config_filename}').expanduser().resolve()
config_system = Path(f'/etc/default/{config_filename}').resolve()

logging_config = Path('./logging.cfg').resolve()




# Plugins Information
plugins = 'plugins'

## WaveShare Information
ws_version = '751a9fb 2020-09-04 15:30:45 +0800'

# local version of waveshare library
waveshare_epd = 'waveshare_epd'

## Runtime Constants
absolute_path = Path(__file__).absolute().parent
