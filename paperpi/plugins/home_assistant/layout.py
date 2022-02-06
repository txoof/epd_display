import os
dir_path = os.path.dirname(os.path.realpath(__file__))

four_sensors_and_media_player = {
      'entity1': {
          'type': 'TextBlock',
          'image': False,
          'max_lines': 1,
          'width': 1/2,
          'height': 0.2,
          'padding': 20,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (0, 0),
          'relative': False
      },
      'entity3': {
          'type': 'TextBlock',
          'image': False,
          'max_lines': 1,
          'width': 1/2,
          'height': 0.2,
          'padding': 20,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (None, 0),
          'relative': ['entity1', 'entity3']
      },
      'entity2': {
          'type': 'TextBlock',
          'image': False,
          'max_lines': 1,
          'width': 1/2,
          'height': 0.2,
          'padding': 20,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (0, None),
          'relative': ['entity2', 'entity1'],
          'border_config': {'fill': 0,
                            'width': 3,
                            'sides': ['bottom']}
      },
      'entity4': {
          'type': 'TextBlock',
          'image': False,
          'max_lines': 1,
          'width': 1/2,
          'height': 0.2,
          'padding': 20,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (None, None),
          'relative': ['entity2', 'entity3'],
          'border_config': {'fill': 0,
                            'width': 3,
                            'sides': ['bottom']}

      },
      'media': {
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'padding': 20,
          'width': 1/2,
          'height': 0.18,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (0, None),
          'relative': ['media', 'entity2']
      },
      'title': {
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'padding': 20,
          'width': 1/2,
          'height': 0.15,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (0, None),
          'relative': ['title', 'media']
      },
      'artist': {
          'type': 'TextBlock',          
          'image': False,
          'max_lines': 1,
          'padding': 20,
          'width': 1/2,
          'height': 0.15,
          'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
          'abs_coordinates': (0, None),
          'relative': ['artist', 'title']
      },
      'image': {
          'type': 'ImageBlock',         
          'image': True,
          'width': 1,
          'height': 0.6,
          'padding': 20,
          'random': True,
          'abs_coordinates': (None, None),
          'relative': ['title', 'entity2']
      }
}

# set the default layout here
layout = four_sensors_and_media_player

