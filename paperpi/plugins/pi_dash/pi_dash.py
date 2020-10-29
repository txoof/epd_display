#!/usr/bin/env python3
# coding: utf-8




import gpiozero
import socket
import logging

try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants






logging.getLogger(__name__)






def update_function(self):
    data = constants.data
    try:
        pi_temp = gpiozero.CPUTemperature()
        pi_load = gpiozero.LoadAverage()
        pi_disk = gpiozero.DiskUsage()
        pi_info = gpiozero.pi_info()
    except gpiozero.GPIOZeroError:
        return data

    
    data = {'temp': f'{int(pi_temp.temperature)}C', 
            'temp_icon': './images/Thermometer_icon.png',
            'load': f'{pi_load.load_average}', 
            'cpu_icon': './images/CPU_icon.png',
            'disk_use': f'{int(pi_disk.usage)}%',  
            'disk_icon': './images/SSD_icon.png',
            'pi_model': f'Pi {pi_info.model} rev {pi_info.revision}',
            'hostname': socket.gethostname()}
    
    return data






# layout = {
#     'hostname': {
#         'image': None,
#         'max_lines': 1,
#         'width': 1,
#         'height': 1/6,
#         'abs_coordinates': (0, 0),
#         'hcenter': True,
#         'vcenter': True,
#         'font': '../../fonts/Sarabun/Sarabun-Regular.ttf'
#     },
#     'temp_icon': {
#         'image': True,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates':(0, None),
#         'relative': ('temp_icon', 'hostname'),
#         'hcenter': True,
#         'vcenter': True,
#         'padding': 4
#     },
#     'temp': {
#         'image': None,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates': (None, None),
#         'relative': ('temp_icon', 'hostname'),
#         'font': '../../fonts/Sarabun/Sarabun-Regular.ttf',
#         'hcenter': False,
#         'vcenter': True
#     },
#     'cpu_icon': {
#         'image': True,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates':(0, None),
#         'relative': ('temp', 'hostname'),
#         'hcenter': True,
#         'vcenter': True,
#         'padding': 4
#     },
#     'load': {
#         'image': None,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates': (None, None),
#         'relative': ('cpu_icon', 'hostname'),
#         'font': '../../fonts/Sarabun/Sarabun-Regular.ttf',
#         'hcenter': False,
#         'vcenter': True
#     },   
#     'disk_icon': {
#         'image': True,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates':(0, None),
#         'relative': ('disk_icon', 'temp_icon'),
#         'hcenter': True,
#         'vcenter': True,
#         'padding': 4
#     },
#     'disk_use': {
#         'image': None,
#         'width': 1/4,
#         'height': 2/6,
#         'abs_coordinates': (None, None),
#         'relative': ('disk_icon', 'temp'),
#         'font': '../../fonts/Sarabun/Sarabun-Regular.ttf',
#         'hcenter': True,
#         'vcenter': True
#     },
#     'pi_model': {
#         'image': None,
#         'max_lines': 1,
#         'width': 1,
#         'height': 1/6,
#         'abs_coordinates': (0, None),
#         'hcenter': True,
#         'vcenter': True,
#         'relative': ('pi_model', 'disk_icon'),
#         'font': '../../fonts/Sarabun/Sarabun-Regular.ttf'
#     },    
# }



