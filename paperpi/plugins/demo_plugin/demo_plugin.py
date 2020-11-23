#!/usr/bin/env python3
# coding: utf-8






# your function must import layout and constants
# this is structured to work both in Jupyter notebook and from the command line
try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants
    
from random import randrange
from datetime import datetime
from pathlib import Path






def demo_function(*args, **kwargs):
    '''demo function that prints a docstring
    
    This function prints the __doc__ string for this function as a 
    demonstration of a Plugin "user-facing" function.
    
    Args:
        None
        
    Returns:
        None
    %U'''
    
    print(demo_function.__doc__)






def useless_function():
    '''useless function that does nothing
    
    This function does nothing, and will be ignored by the documentation 
    generators because it does not end with "%U" on the last line.
    '''
    2 + 2
    pass






# make sure this function can accept *args and **kwargs even if you don't intend to use them
def update_function(self, *args, **kwargs):
    '''update function for demo plugin providing some silly information and a picture
    
    This plugin provides a message generated for the user and 
    a static image that floats around
    
    Requirments:
        self.config(dict): {
            'your_name': 'user name',
            'your_color': 'user color',
        }
        
    Args: 
        self(namespace): namespace from plugin object
    
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))

    # Don't forget to end your docstring with a "%U" so it is displayed
    %U'''   
    
    # pull information from the plugin section of the configuration file (slimpi.ini)
    name = self.config['your_name']
    color = self.config['favorite_color']
    
    # do something with the configuration data
    strings = [
        f'Hi {name}! I hear your color is {color}',
        f'{name}, did you know your color has {len(color)} characters in it?',
        f'Your name spelled backards is "{name[::-1]}"',
        f'If you sort your favorite color alphabetically, you get: {("").join(sorted(color))}',
        f'If you sort your name alphabetically, you get: {("").join(sorted(name))}',
    ]
    
    # define the components of the data that will be returned
    my_string = strings[randrange(0, len(strings)-1)]
    time = datetime.now().strftime("%H:%M")
    minute = datetime.now().strftime("%M")
    image = Path(constants.img_file).resolve()

    # optionally raise the priority under certain circumstances
    
    # if the minute is even, raise the priority, else, leave it at the normal priority
    if int(minute) % 2 == 0:
        priority = self.max_priority - 1
        extra_string = 'The minute is EVEN! I will raise the priority!'
    else:
        priority = self.max_priority
        extra_string = ':[ nothing :['
    
    # build the output
    is_updated = True
    data = {
        'string': my_string,
        'time': time,
        'extra': extra_string,
        'image': image
    }
    priority = priority
    
    
    return (is_updated, data, priority)








# update_function(self)








# from library import SelfDummy

# self = SelfDummy()
# self.config = {'your_name': 'Aaron', 'favorite_color': 'pink'}

