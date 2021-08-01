# librespot_client/lms_client layouts
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

two_rows_text_only = {
    'title':
            {'image': None,
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
            {'image': None,
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

# two_column_three_row = {
#       'coverart': {
#             'image': True,
#             'max_lines': None,
#             'padding': 8,
#             'width': 1/3,
#             'height': .6,
#             'abs_coordinates': (0, 0),
#             'hcenter': True,
#             'vcenter': True,
#             'relative': False,
#             'mode': 'L',
#       },
#       'title': {
#             'image': None,
#             'max_lines': 3,
#             'padding': 1,
#             'width': 2/3,
#             'height': .6,
#             'abs_coordinates': (None, 0),
#             'relative': ['coverart', 'title'],
#             'hcenter': False,
#             'vcenter': True,
#             'mode': 'L',
#             'font': dir_path+'/../../fonts/Oswald/static/Oswald-Regular.ttf',
          
#       },
#       'artist': {
#             'image': None,
#             'max_lines': 2,
#             'padding': 4,
#             'width': 1,
#             'height': .31,
#             'abs_coordinates': (0, None),
#             'relative': ['artist', 'title'],
#             'hcenter': True,
#             'vcenter': True,
#             'align': 'center',
#             'mode': 'L',
# #             'font': dir_path+'/../../fonts/Open_Sans/OpenSans-SemiBold.ttf',
#             'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf',
#       },
#       'album': {
#             'image': None,
#             'max_lines': 1,
#             'padding': 4,
#             'width': 1,
#             'height': .09,
#             'abs_coordinates': (0, None),
#             'relative': ['album', 'artist'],
#             'hcenter': True,
#             'vcenter': True,
#             'align': 'center',
#             'mode': 'L',
#             'font': dir_path+'/../../fonts/Open_Sans/OpenSans-SemiBold.ttf',
#             'font': dir_path+'/../../fonts/Montserrat/Montserrat-SemiBold.ttf',          
#       }
# }


# default layout
layout = two_column_three_row
