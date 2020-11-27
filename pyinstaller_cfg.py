# base path that contains the project
base_path = './paperpi'
# entrance script for program
base_script = 'paperpi.py'

plugin_path = './paperpi/plugins'

# command additional options
options = [
  '-F',
  '--noconfirm',
  '--clean',
]

hidden_imports = [
  'spidev',
  'RPi',
  'RPi.GPIO',
]

# data files and directories to include
# tuples (source, dest)
datas = [
  ('./config', './config'),
  ('./constants.py', './' ),
  ('./fonts', './fonts'),
  ('./library', './library'),
  ('./plugins', './plugins'),
  ('./waveshare_epd', './waveshare_epd'),
]

# modules to exclude
exclude = [
  ''
]
