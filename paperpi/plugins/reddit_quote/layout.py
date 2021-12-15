# handling file locations with relative paths is hard
# this simplifies locating the fonts needed for this layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

quote_small_screen = {
      'text': {
          'mode': 'L',          
          'type': 'TextBlock',
          'image': False,
          'max_lines': 5,
          'width': 1,
          'height': .7,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
          'hcenter': True,
          'vcenter': True,
          'align': 'left',
          'padding': 5,
          # absolute coordinates of the text block (top left is 0,0)
          'abs_coordinates': (0, 0),
          # coordinates are not calculated relative to another block
          'relative': False
      },
      # this block will contain the string provided by  data['time']
      'attribution': {
          'mode': 'L',          
          'type': 'TextBlock',
          'image': False,
          'max_lines': 2,
          'width': 1,
          'height': .3,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Regular.ttf',          
          'hcenter': True,
          'vcenter': True,
          'align': 'center',
          'padding': 5,
#           'border_config': {'fill': 0, 'width': 3, 'sides': ['top']},
          'abs_coordinates': (0, None),
          'relative': ('attribution', 'text'),
      },
}



quote = {
      'text': {
          'mode': 'L',          
          'type': 'TextBlock',
          'image': False,
          'max_lines': 6,
          'width': 1,
          'height': .65,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
          'hcenter': True,
          'vcenter': True,
          'align': 'left',
          'padding': 20,
          # absolute coordinates of the text block (top left is 0,0)
          'abs_coordinates': (0, 0),
          # coordinates are not calculated relative to another block
          'relative': False
      },
      # this block will contain the string provided by  data['time']
      'attribution': {
          'mode': 'L',          
          'type': 'TextBlock',
          'image': False,
          'max_lines': 2,
          'width': 1,
          'height': .25,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Regular.ttf',          
          'hcenter': True,
          'vcenter': True,
          'align': 'center',
          'padding': 20,
          'border_config': {'fill': 0, 'width': 3, 'sides': ['top']},
          'abs_coordinates': (0, None),
          'relative': ('attribution', 'text'),
      },
      'time': {
          'mode': 'L',          
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'width': 1,
          'height': .1,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
          # X coordinate is absolute, Y is calculated
          'abs_coordinates': (0, None),
          # Use X from 'time', Y from the bottom of 'string'
          'relative': ['time', 'attribution'],
      },
}

quote_inverse = {
      'text': {
          'mode': 'L',
          'type': 'TextBlock',
          'image': False,
          'max_lines': 6,
          'width': 1,
          'height': .65,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
          'hcenter': True,
          'vcenter': True,
          'align': 'left',
          'padding': 20,
          # absolute coordinates of the text block (top left is 0,0)
          'abs_coordinates': (0, 0),
          # coordinates are not calculated relative to another block
          'relative': False,
          'inverse': True
      },
      # this block will contain the string provided by  data['time']
      'attribution': {
          'mode': 'L',          
          'type': 'TextBlock',
          'image': False,
          'max_lines': 2,
          'width': 1,
          'height': .25,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Regular.ttf',          
          'hcenter': True,
          'vcenter': True,
          'align': 'center',
          'padding': 20,
          'border_config': {'fill': 255, 'width': 3, 'sides': ['top']},
          'abs_coordinates': (0, None),
          'relative': ('attribution', 'text'),
          'inverse': True          
      },
      'time': {
          'mode': 'L',          
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'width': 1,
          'height': .1,
          'random': False,
          'font': dir_path+'/../../fonts/Josefin_Sans/JosefinSans-Light.ttf',
          # X coordinate is absolute, Y is calculated
          'abs_coordinates': (0, None),
          # Use X from 'time', Y from the bottom of 'string'
          'relative': ['time', 'attribution'],
          'inverse': True          
      },
}


# set the default layout here
layout = quote_inverse

