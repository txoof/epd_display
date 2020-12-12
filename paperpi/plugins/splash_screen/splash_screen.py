#!/usr/bin/env python3
# coding: utf-8




try:
    from . import layout
    from . import constants
except ImportError:
    import layout
    import constants11






def update_function(self, app_name, version, url):
    '''update function for splash_screen provides program name, version, url
    
    This plugin provides a basic splash screen with application 
    name, version and url
    
    Requirements:
        None
        
    Args:
        self(`namespace`)
        app_name(`str`): application name
        version(`str`): version number
        url(`str`) url
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))        
    %U'''
    return(True, {'app_name': app_name, 'version': version, 'url': url}, -1)











