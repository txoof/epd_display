# handling file locations with relative paths is hard
# this simplifies locating the fonts needed for this layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

ticker_hd = {
    'update_time': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': 1,
        'height': 0.1,
        'abs_coordinates': (0, 0),
        'hcenter': True,
        'vcenter': True,
        'relative': False,
        'max_lines': 2,
        'padding': 2,
        'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf'
    },
      'coin_file': {
          'type': 'ImageBlock',
          'mode': 'L',
          'image': True,
          'max_lines': 3,
          'width': .15,
          'height': .15,
          'hcenter': True,
          'vcenter': True,
          'abs_coordinates': (0, None),
          'relative': ['coin_file', 'update_time']
      },    
    'price_string': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': .35,
        'height': .2,
        'hcenter': False,
        'vcenter': True,
        'relative': ['coin_file', 'update_time'],
        'abs_coordinates': (None, None),
        'max_lines': 1,
        'font':  dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
        'textwrap': False
    },
    'change_vol_string': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': .35,
        'height': .13,
        'hcenter': False,
        'vcenter': True,
        'abs_coordinates': (None, None),
        'relative': ['coin_file', 'price_string'],
        'max_lines': 2,
        'font':  dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf'
    },
        
    'sparkline': {
        'type': 'ImageBlock',
        'mode': 'L',
        'image': True,
        'width': .50,
        'height': .33,
        'abs_coordinates': (None, None),
        'relative': ['price_string', 'update_time'],
    },
    'qr_code': {
        'type': 'ImageBlock',
        'image': True,
        'mode': 'L',
        'width': .15,
        'height': .57,
        'hcenter': True,
        'vcenter': True,
        'abs_coordinates': (0, None),
        'relative': ['qr_code', 'sparkline']
    },    
    'rss_feed': {
        'type':  'TextBlock',
        'mode': 'L',
        'image': True,
        'width': .85,
        'height': .57,
        'hcenter': True,
        'vcenter': True,
        'max_lines': 5,
            'font': dir_path+'/../../fonts/Lato/Lato-Regular.ttf',
        'abs_coordinates': (None, None),
        'relative': ['qr_code', 'sparkline'],
    },
}

ticker_simple = {
      'coin_file': {
          'type': 'ImageBlock',
          'mode': 'L',
          'image': True,
          'max_lines': 3,
          'width': .3,
          'height': .3,
          'hcenter': True,
          'vcenter': True,
          'abs_coordinates': (0, 0),
          'relative': False
      },    
    'price_string': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': .7,
        'height': .2,
        'hcenter': False,
        'vcenter': True,
        'relative': ['coin_file', 'price_string'],
        'abs_coordinates': (None, 0),
        'max_lines': 1,
        'font':  dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf'
    },
    'change_vol_string': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': 1,
        'height': .1,
        'hcenter': False,
        'vcenter': True,
        'abs_coordinates': (None, None),
        'relative': ['coin_file', 'price_string'],
        'max_lines': 1,
        'font':  dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf'
    },
    'sparkline': {
        'type': 'ImageBlock',
        'mode': 'L',
        'image': True,
        'width': 1,
        'height': .55,
        'abs_coordinates': (0, None),
        'hcenter': True,
        'vcenter': True,
        'relative': ['sparkline', 'coin_file'],
    },
   'update_time': {
        'type': 'TextBlock',
        'mode': 'L',
        'image': False,
        'width': 1,
        'height': 0.15,
        'abs_coordinates': (0, None),
        'hcenter': True,
        'vcenter': True,
        'relative': ['update_time', 'sparkline'],
        'max_lines': 2,
        'padding': 2,
        'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf' },    
}

# set the default layout here
layout = ticker_hd

