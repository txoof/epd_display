# lms_client layouts
# handling file locations with relative paths is hard
# this simplifies locating the fonts needed for this layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# this is the layout that the Screen() module will use
# to format the output of your plugin
my_layout_one = {
      # each "block" of the screen is defined as a keyword 
      # that matches a keyword from the data returned by the plugin
      'string': {
          # this block is of a TextBlock type
          'type': 'TextBlock',
          # this block does not contain an image
          'image': False,
          # number of lines of text to display before word-wrapping
          'max_lines': 3,
          # width of text block as fraction of entire display
          'width': 1,
          # height of text block as fraction of entire display
          'height': 1/2,
          # randomize the placement of the text within the block
          'random': True,
          # font to use -- append dir_path to the font to make the
          # relative path work properly 
          'font': dir_path+'/../../fonts/BenchNine/BenchNine-Regular.ttf',
          # absolute coordinates of the text block (top left is 0,0)
          'abs_coordinates': (0, 0),
          # coordinates are not calculated relative to another block
          'relative': False
      },
      # this block will contain the string provided by  data['time']
      'time': {
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'width': 1/2,
          'height': 1/4,
          'random': True,
          'font': dir_path+'/../../fonts/BenchNine/BenchNine-Regular.ttf',
          # X coordinate is absolute, Y is calculated
          'abs_coordinates': (0, None),
          # Use X from 'time', Y from the bottom of 'string'
          'relative': ['time', 'string'],
      },
      'extra': {
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 3,
          'width': 1/2,
          'height': 1/4,
          'random': True,
          'font': dir_path+'/../../fonts/BenchNine/BenchNine-Regular.ttf',
          # X coordinate is absolute, Y is calculated
          'abs_coordinates': (0, None),
          'relative': ['extra', 'time']
      },
      'image': {
          'type': 'ImageBlock',         
          'image': True,
          'width': 1/2,
          'height': 1/2,
          'random': True,
          # X and Y are calculated
          'abs_coordinates': (None, None),
          # calculate relative to the right side of 'time' (X) and 
          # bottom of 'string' (Y)
          'relative': ['time', 'string']
      }
}

# set the default layout here
layout = my_layout_one

