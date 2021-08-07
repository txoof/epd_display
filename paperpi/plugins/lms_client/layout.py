# librespot_client/lms_client layouts
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

two_rows_text_only = {
    'title':
            {'type': 'TextBlock',
             'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': .8,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'align': 'center',
             'relative': False,
             'font': dir_path+'/../../fonts/Oswald/static/Oswald-Regular.ttf',
             'font_size': None},

    'artist':
            {'type': 'TextBlock',
             'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': .2,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['artist', 'title'],
             'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf',
             'font_size': None},
}


three_rows_text_only = {
    'title': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 2,
        'padding': 5,
        'width': 1,
        'height': .75,
        'abs_coordinates': (0, 0),
        'hcenter': True,
        'vcenter': True,
        'align': 'left',
        'relative': False,
        'mode': 'L',
        'font': dir_path+'/../../fonts/Oswald/static/Oswald-Medium.ttf'
    },
    'artist': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 2,
        'width': 1,
        'height': .18,
        'abs_coordinates': (0, None),     
        'hcenter': True,
        'vcenter': True,
        'relative': ['artist', 'title'],
        'mode': 'L',
        'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf'
    },
    'album': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 1,
        'width': 1,
        'height': .07,
        'abs_coordinates': (0, None),
        'hcenter': True,
        'vcenter': True,
        'relative': ['album', 'artist'],
        'mode': 'L',
        'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf'
    },     
}

two_column_three_row = {
    'coverart': {
        'type': 'ImageBlock',
        'image': True,
        'mode': 'L',
        'padding': 5,
        'width':.4,
        'height': .5,
        'vcenter': True,
        'hcenter': True,
        'relative': False,
        'abs_coordinates': (0, 0)
    },
    'artist': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 3,
        'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf',
        'mode': 'L',
        'vcenter': True,
        'hcenter': False,
        'align': 'left',
        'padding': 5,
        'width': .6,
        'height': .40,
        'relative': ['coverart', 'artist'],
        'abs_coordinates': (None, 0),
        
    },
    'album': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 2,
        'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf',
        'mode': 'L',
        'vcenter': True,
        'hcenter': False,
        'align': 'left',
        'padding': 5,
        'width': .6,
        'height': .1,
        'relative': ['coverart', 'artist'],
        'abs_coordinates': (None, 0),
        
    },
    'title': {
        'type': 'TextBlock',
        'image': False,
        'max_lines': 2,
        'font': dir_path+'/../../fonts/Oswald/static/Oswald-Medium.ttf',
        'mode': 'L',
        'vcenter': True,
        'hcenter': True,
        'align': 'left',
        'padding': 5,
        'width': 1,
        'height': .5,
        'relative': ['title', 'album'],
        'abs_coordinates': (0, None)
    },
}
layout = two_column_three_row