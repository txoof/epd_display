import os
dir_path = os.path.dirname(os.path.realpath(__file__))
img_path = dir_path+'/images'
version = '0.1.0'
name = 'pi_dash'
data  = {'temp': '0',
         'temp_icon': dir_path+'/./images/Thermometer_icon.png',
         'load': '0.0', 
         'cpu_icon': dir_path+'/./images/CPU_icon.png',
         'disk_use': '0%',  
         'disk_icon': dir_path+'/./images/SSD_icon.png',
         'pi_model': 'Unknown',
         'hostname': 'Unknown'}


sample_config = '''
[Plugin: Pi Dashboard]
layout = layout
plugin = pi_dash
refresh_rate = 25
min_display_time = 30
max_priority = 2
'''
