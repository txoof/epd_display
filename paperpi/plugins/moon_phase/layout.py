# lms_client layouts
# handling file locations with relative paths is hard
# this simplifies locating the fonts needed for this layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# this is the layout that the Screen() module will use
# to format the output of your plugin
moon_only = {
      # each "block" of the screen is defined as a keyword 
      # that matches a keyword from the data returned by the plugin
  'image_file': {
      'type': 'ImageBlock',
      'mode': 'L',
      # this block does not contain an image
      'image': True,
      # width of block as fraction of entire display
      'width': 1,
      # height of block as fraction of entire display
      'height': 1,
      # absolute coordinates of the text block (top left is 0,0)
      'abs_coordinates': (0, 0),
      # coordinates are not calculated relative to another block
      'relative': False,
      'hcenter': True,
      'vcenter': True,
      'bkground': 0,
    },
}

moon_data = {
   'moonrise': {
       'type': 'TextBlock',
       'mode': 'L',
       'image': False,
       'width': .5,
       'height': .06,
       'abs_coordinates': (0, 0),
       'relative': False,
       'hcenter': False,
       'vcenter': True,
       'inverse': True,
       'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
   },    
   'moonset': {
       'type': 'TextBlock',
       'mode': 'L',
       'image': False,
       'width': .5,
       'height': .06,
       'abs_coordinates': (None, 0),
       'relative': ('moonrise', 'moonset'),
       'hcenter': False,
       'vcenter': True,
       'inverse': True,
       'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',       
   },
   'image_file': {
      'type': 'ImageBlock',
      'mode': 'L',
      # this block does not contain an image
      'image': True,
      # width of block as fraction of entire display
      'width': 1,
      # height of block as fraction of entire display
      'height': .84,
      # absolute coordinates of the text block (top left is 0,0)
      'abs_coordinates': (0, None),
      # coordinates are not calculated relative to another block
      'relative': ('image_file', 'moonrise'),
      'hcenter': True,
      'vcenter': True,
      'bkground': 0,
   },
   'phase_desc': {
       'type': 'TextBlock',
       'mode': 'L',
       'image': False,
       'width': 1,
       'height': .1,
       'abs_coordinates': (0, None),
       'relative': ('phase_desc', 'image_file'),
       'hcenter': True,
       'vcenter': True,
       'inverse': True,
       'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',       
   }
}
# set the default layout here
layout = moon_data
