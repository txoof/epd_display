# basic clock layout
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


basic_clock = {
    'digit_time': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 2,
        'width': 1,
        'height': 1,
        'abs_coordinates': (0, 0),
        'rand': True,
        'font': dir_path+'/../../fonts/Kanit/Kanit-Medium.ttf',
        'mode': 'L'
    },
}

# set the default layout here
layout = basic_clock
