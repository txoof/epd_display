# decimal binary clock
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

dec_binary_clock = {
    'bin_img':
            {'image': True,
             'max_lines': None,
             'padding': 5,
             'width': 1,
             'height': 8/9,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'rand': False,
             'inverse': False,
             'relative': False
            },
    'time':
          {'image': None,
           'max_lines': 1,
           'padding': 5,
           'width': 1,
           'height': 1/9,
           'abs_coordinates': (0, None),
           'hcenter': False,
           'vcenter': False,
           'rand': True,
           'inverse': False,
           'relative': ['time', 'bin_img'],
           'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
           'font_size': None},
}

# default layout
layout = dec_binary_clock
