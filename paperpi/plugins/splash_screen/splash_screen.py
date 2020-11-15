#!/usr/bin/env python3
# coding: utf-8




try:
    from . import layout
    from . import constants
#     from . import constants_spot
except ImportError:
    import layout
    import constants
#     import constants_spot






def update_function(self, app_name, version, url):
    '''update function for splash_screen
    provides a basic splash screen with application name, version and url
    
    Requirements:
        None
        
    Args:
        self(`namespace`)
        app_name(`str`): application name
        version(`str`): version number
        url(`str`) url
    %U'''
    return(True, {'app_name': app_name, 'version': version, 'url': url}, -1)











