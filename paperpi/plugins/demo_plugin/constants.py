version = '0.1.0'
name = 'demo_plugin'
data = {
    'welcome_str': 'welcome string',
    'time': 'time in HH:MM format',
    'img': 'a static image',
}
sample_config = '''
# this is a sample config users can use to help setup the plugin
[Plugin: A Demo Plugin]
# default layout
layout = layout
# the literal name of your module
plugin = demo_plugin
# recommended display time
min_display_time = 30
# maximum priority in display loop
max_priority = 1
# your name
your_name = Txoof
# your favorite color
your_color = chartreuse
'''
