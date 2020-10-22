from pathlib import Path
# rebuild with multiple options
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
                'font': Path('../../fonts/Open_Sans/OpenSans-Regular.ttf').absolute(),
                'font_size': None # font size to use for text
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
                'font': Path('../../fonts/Open_Sans/OpenSans-Regular.ttf').absolute(),
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
                'font': Path('../../fonts/Open_Sans/OpenSans-Regular.ttf').absolute(),
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
                'font': Path('../../fonts/Open_Sans/OpenSans-Regular.ttf').absolute(),
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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
             'font_size': None},

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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
             'font_size': None},
    'mode':
            {'image': False,
             'max_lines': 1,
             'width': 3/5,
             'height': 1/18,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'rand': True,
             'relative': ['coverart', 'album'],
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
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
             'font': Path('../../fonts/Anton/Anton-Regular.ttf').absolute(),
             'font_size': None},
}
