# librespot_client/lms_client layouts
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

three_rows_text_only = {
    'title': {
        'image': False,
        'max_lines': 2,
        'padding': 0,
        'width': 1,
        'height': 4/7,
        'abs_coordinates': (0, 0),
        'hcenter': True,
        'vcenter': True,
        'relative': False,
        'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf'
    },
    'artist': {
        'image': False,
        'max_lines': 2,
        'width': 1,
        'height': 2/7,
        'abs_coordinates': (0, None),     
        'hcenter': True,
        'vcenter': True,
        'relative': ['artist', 'title'],
        'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf'
    },
    'album': {
        'image': False,
        'max_lines': 1,
        'width': 1,
        'height': 1/7,
        'abs_coordinates': (0, None),
        'hcenter': True,
        'vcenter': True,
        'relative': ['album', 'artist'],
        'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf'
    },     
}

twoColumnThreeRows = {
      'coverart': {
            'image': True,
            'max_lines': None,
            'padding': 5,
            'width': 1/3,
            'height': 4/7,
            'abs_coordinates': (0, 0),
            'hcenter': True,
            'vcenter': True,
            'relative': False,
            'mode': 'L',          
      },
      'title': {
            'image': None,
            'max_lines': 2,
            'padding': 4,
            'width': 2/3,
            'height': 4/7,
            'abs_coordinates': (None, 0),
            'relative': ['coverart', 'title'],
            'hcenter': True,
            'vcenter': True,
            'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
      },
      'artist': {
            'image': None,
            'max_lines': 2,
            'padding': 4,
            'width': 1,
            'height': 2/7,
            'abs_coordinates': (0, None),
            'relative': ['artist', 'title'],
            'hcenter': True,
            'vcenter': True,
            'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
            #'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
      },
      'album': {
            'image': None,
            'max_lines': 1,
            'padding': 4,
            'width': 1,
            'height': 1/7,
            'abs_coordinates': (0, None),
            'relative': ['album', 'artist'],
            'hcenter': True,
            'vcenter': True,
            'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
            #'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
      },


}


twoColumn = {
    'coverart': { # coverart image
                'image': True, # has an image that may need to be resized
                'max_lines': None, # number of lines of text associated with this section
                'padding': 10, # amount of padding at edge
                'width': 1/3, # fraction of total width of display
                'height': 1, # fraction of total height
                'abs_coordinates': (0, 0), # X, Y for top left position of section
                'hcenter': True, # horizontal center-align the contents
                'vcenter': True, # vertically center-align the contents
                'relative': False, # False if position is absolute
                'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None, # font size to use for text
                'mode': 'L',            
    },
    'title': { # track title
                'image': None, # none if no image is needed
                'max_lines': 3, # number of lines of text associated with this section
                'padding': 10,  # padding at edge
                'width': 2/3, # fraction of total width of display
                'height': 3/5, # fraction of total height of display
                'abs_coordinates': (None, 0), # X, Y for top left position of section
                                          # None indicates that the position is not
                                          # known and will be calculated
                                          # relative to another section
                                          # integer indicates an absolute position to use
                'hcenter': False, # horizontal center-align the contents
                'vcenter': True, # vertically center-align the contents
                'relative': ['coverart', 'title'], # [X Section: abs_coordinates+dimension
                                                   #, Y section abs_coordinates+dimension]
                'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None # font size to use for text

    },
    'artist': { # track artist
                'image': None,
                'max_lines': 2,
                'padding': 10,
                'width': 2/3,
                'height': 1/5,
                'abs_coordinates': (None, None),
                'hcenter': False,
                'vcenter': True,
                'relative': ['coverart', 'title'],
                'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None
    },
    'album': { #album name
                'image': None,
                'max_lines': 2,
                'padding': 10,
                'width': 2/3,
                'height': 1/5,
                'abs_coordinates': (None, None),
                'hcenter': False,
                'vcenter': True,
                'relative': ['coverart', 'artist'],
                'font': dir_path+'/../../fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None
    }
}

threeRowLarge = {
    'title':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': 6/9,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'relative': False,
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'coverart':
            {'image': True,
             'max_lines': None,
             'padding': 2,
             'width': 2/5,
             'height': 3/9,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['coverart', 'title'],
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None,
             'mode': 'L',},

    'artist':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 3/18,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'relative': ['coverart', 'title'],
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'album':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 2/18,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'relative': ['coverart', 'artist'],
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'mode':
            {'image': False,
             'max_lines': 1,
             'width': 3/5,
             'height': 1/18,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'rand': False,
             'relative': ['coverart', 'album'],
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None}
}

twoRowSmall = {
    'title':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': 2/3,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'relative': False,
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None},

    'artist':
            {'image': None,
             'max_lines': 1,
             'padding': 10,
             'width': 1,
             'height': 1/3,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['artist', 'title'],
             'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
}

# default layout
layout = twoColumnThreeRows
