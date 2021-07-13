import os
dir_path = os.path.dirname(os.path.realpath(__file__))

default = {
    'comic': {
        'image': True,
        'width': 1,
        'height': .75,
        'abs_coordinates': (0, 0),
        'padding': 5,
        'hcenter': True,
        'vcenter': True,
        'mode': 'L'
    },
    'caption': {
        'image': False,
        'width': 1,
        'height': .2,
        'padding': 5,
        'abs_coordinates': (0, None),
        'relative': ['caption', 'comic'],
        'hcenter': True,
        'vcenter': True,
        'max_lines': 3,
        'mode': 'L',
        'font': dir_path+'/../../fonts/LibreCaslonText/LibreCaslonText-Italic.ttf'  
    },
    'time': {
        'image': False,
        'width': 1,
        'height': .05,
        'abs_coordinates': (0, None),
        'relative': ['time', 'caption'],
        'hcenter': False,
        'vcenter': False,
        'rand': False,
        'mode': 'L',
        'padding': 5,
        'font': dir_path+'/../../fonts/Anton/Anton-Regular.ttf'
    }
    
}

# default layout
layout = default
