version='0.1.0'
name = 'decimal binary clock'

data = {
    'bin_img': 'PIL Image',
    'time': 'system time as string HH:MM',
}

sample_config ='''
[Plugin: decimal binary clock]
layout = layout
plugin = dec_bin_clock
refresh_rate = 55
min_display_time = 60
max_priority = 2
'''
