# xkcd layouts
# handling file locations with relative paths is hard
# this simplifies locating the fonts needed for this layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# this is the layout that the Screen() module will use
# to format the output of your plugin
comic_only = {
      'image_file': {
          'type': 'ImageBlock',
          'mode': 'L',
          'image': True,
          'max_lines': 3,
          'width': 1,
          'height': 1,
          'random': False,
          'hcenter': True,
          'vcenter': True,
          'abs_coordinates': (0, 0),
          'relative': False
      },
}

comic_title = {
      'image_file': {
          'type': 'ImageBlock',
          'mode': 'L',
          'image': True,
          'max_lines': 3,
          'width': 1,
          'height': .82,
          'random': False,
          'hcenter': True,
          'vcenter': True,
          'abs_coordinates': (0, 0),
          'relative': False
      },
     'safe_title': {
          'type': 'TextBlock',
          'mode': 'L',
          'image': False,
          'width': 1,
          'height': .2,
          'hcenter': True,
          'vcenter': True,
          'font': dir_path+'/../../fonts/Lato/Lato-Bold.ttf',        
          'max_lines': 2,
          'abs_coordinates': (0, None),
          'relative': ('safe_title', 'image_file'),
     }
}


comic_title_alttext = {
      'image_file': {
          'type': 'ImageBlock',
          'mode': 'L',
          'image': True,
          'max_lines': 3,
          'width': 1,
          'height': .75,
          'random': False,
          'hcenter': True,
          'vcenter': True,
          'abs_coordinates': (0, 0),
          'relative': False
      },
     'safe_title': {
          'type': 'TextBlock',
          'mode': 'L',
          'image': False,
          'width': 1,
          'height': .1,
          'hcenter': True,
          'vcenter': True,
          'font': dir_path+'/../../fonts/Lato/Lato-Bold.ttf',        
          'max_lines': 1,
          'abs_coordinates': (0, None),
          'relative': ('safe_title', 'image_file'),
     },
     'alt': {
          'type': 'TextBlock',
          'mode': 'L',
          'image': False,
          'width': 1,
          'height': .15,
          'hcenter': True,
          'vcenter': True,
          'font': dir_path+'/../../fonts/Lato/Lato-Italic.ttf',        
          'max_lines': 3,
          'abs_coordinates': (0, None),
          'relative': ('alt', 'safe_title'),
     },

}

# set the default layout here
layout = comic_title_alttext