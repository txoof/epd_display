import os
dir_path = os.path.dirname(os.path.realpath(__file__))

word_clock_lg = {
  'wordtime':
         {'type': 'TextBlock', 
          'image': None,
          'max_lines': 3,
          'padding': 5,
          'width': 1,
          'height': 9/10,
          'abs_coordinates': (0, 0),
          'hcenter': False,
          'vcenter': False,
          'rand': True,
          'inverse': True,
          'relative': False,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'mode': 'L',
          'font_size': None},
  'time':
         {'type': 'TextBlock', 
          'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1,
          'height': 1/10,
          'abs_coordinates': (0, None),
          'vcenter': False,
          'inverse': True,
          'rand': True,
          'relative': ['time', 'wordtime'],
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'mode': 'L',       
          'font_size': None},
}

word_clock = {
  'wordtime':
         {'type': 'TextBlock', 
          'image': None,
          'max_lines': 3,
          'padding': 10,
          'width': 1,
          'height': 6/7,
          'abs_coordinates': (0, 0),
          'hcenter': False,
          'vcenter': False,
          'rand': True,
          'inverse': True,
          'relative': False,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'mode': 'L',
          'font_size': None},
  'time':
         {'type': 'TextBlock', 
          'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1,
          'height': 1/7,
          'abs_coordinates': (0, None),
          'vcenter': False,
          'inverse': True,
          'rand': True,
          'relative': ['time', 'wordtime'],
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'mode': 'L',          
          'font_size': None},
}

# set default layout here
layout = word_clock_lg
