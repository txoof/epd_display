# entrance script for program
base_script = 'paperpi.py'

# command additional options
options = [
  '-F',
  ''
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
