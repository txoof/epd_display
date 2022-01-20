# collect data files - this should reside in a hook file, but I can't get that to work
from PyInstaller.utils.hooks import collect_data_files
# base path that contains the project
base_path = './paperpi'
# entrance script for program
base_script = 'paperpi.py'
#base_script = 'foo.py'

plugin_path = './paperpi/plugins'

# command additional options
options = [
  '-D',
  '--noconfirm',
  '--clean',
  '--additional-hooks-dir=.',
]

hidden_imports = [
  'spidev',
  'RPi',
  'RPi.GPIO',
  'pygal',
]

# datas associated with modules

# data files and directories to include
# tuples (source, dest)


datas = [
  ('./config', './config'),
  ('./my_constants.py', './' ),
  ('./fonts', './fonts'),
  ('./library', './library'),
  ('./plugins', './plugins'),
  ('./waveshare_epd', './waveshare_epd'),
]

# datas that are external to the project (e.g. module datas)
external_module_datas = ['pygal']
external_datas = []

for i in external_module_datas:
  external_datas.extend(collect_data_files(i))

# modules to exclude
exclude = [
  'IPython'
]
