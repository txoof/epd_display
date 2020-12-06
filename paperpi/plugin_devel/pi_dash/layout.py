import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# set default layout 

layout = {
    'hostname': {
        'image': None,
        'max_lines': 1,
        'width': 1,
        'height': 1/6,
        'abs_coordinates': (0, 0),
        'hcenter': True,
        'vcenter': True,
        'font': dir_path+'/../../fonts/Sarabun/Sarabun-Regular.ttf'
    },
    'temp_icon': {
        'image': True,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates':(0, None),
        'relative': ('temp_icon', 'hostname'),
        'hcenter': True,
        'vcenter': True,
        'padding': 4
    },
    'temp': {
        'image': None,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates': (None, None),
        'relative': ('temp_icon', 'hostname'),
        'font': dir_path+'/../../fonts/Sarabun/Sarabun-Regular.ttf',
        'hcenter': False,
        'vcenter': True
    },
    'cpu_icon': {
        'image': True,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates':(0, None),
        'relative': ('temp', 'hostname'),
        'hcenter': True,
        'vcenter': True,
        'padding': 4
    },
    'load': {
        'image': None,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates': (None, None),
        'relative': ('cpu_icon', 'hostname'),
        'font': dir_path+'/../../fonts/Sarabun/Sarabun-Regular.ttf',
        'hcenter': False,
        'vcenter': True
    },   
    'disk_icon': {
        'image': True,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates':(0, None),
        'relative': ('disk_icon', 'temp_icon'),
        'hcenter': True,
        'vcenter': True,
        'padding': 4
    },
    'disk_use': {
        'image': None,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates': (None, None),
        'relative': ('disk_icon', 'temp'),
        'font': dir_path+'/../../fonts/Sarabun/Sarabun-Regular.ttf',
        'hcenter': False,
        'vcenter': True
    },
    'pi_model': {
        'image': None,
        'max_lines': 1,
        'width': 1,
        'height': 1/6,
        'abs_coordinates': (0, None),
        'hcenter': True,
        'vcenter': True,
        'relative': ('pi_model', 'disk_icon'),
        'font': dir_path+'/../../fonts/Sarabun/Sarabun-Regular.ttf'
    },
    'pi_logo': {
        'image': True,
        'width': 1/4,
        'height': 2/6,
        'abs_coordinates': (None, None),
        'relative': ('disk_use', 'cpu_icon'),
        'hcenter': True,
        'vcenter': True,
    },
}
