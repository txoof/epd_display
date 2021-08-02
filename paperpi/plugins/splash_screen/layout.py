import os
dir_path = os.path.dirname(os.path.realpath(__file__))

layout =  {
  'app_name': {
            'image': None,
            'max_lines': 1,
            'padding': 10,
            'width': 1,
            'height': 6/10,
            'abs_coordinates': (0, 0),
            'hcenter': True,
            'vcenter': True,
            'rand': False,
            'inverse': False,
            'relative': False,
            'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
            'mode': '1',
            'font_size': None},

  'version':
          {'image': None,
           'max_lines': 1,
           'padding': 10,
           'width': 1,
           'height': 1/10,
           'abs_coordinates': (0, None),
           'hcenter': True,
           'vcenter': True,
           'rand': False,
           'inverse': False,
           'relative': ['version', 'app_name'],
           'font': dir_path+'/../../fonts/Dosis/static/Dosis-SemiBold.ttf',
           'font_size': None,
           'mode': '1'},

  'url':
          {'image': None,
           'max_lines': 2,
           'padding': 10,
           'width': 1,
           'height': 3/10,
           'abs_coordinates': (0, None),
           'hcenter': True,
           'vcenter': True,
           'rand': False,
           'inverse': False,
           'relative': ['url', 'version'],
           'font': dir_path+'/../../fonts/Dosis/static/Dosis-SemiBold.ttf',
           'maxchar': 35,
           'font_size': None,
           'mode': '1'}
}
