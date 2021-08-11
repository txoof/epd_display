#!/usr/bin/env python3
# coding: utf-8




import logging






# two different import modes for development or distribution
try:
    # import from other modules above this level
    from . import layout
    from . import constants
except ImportError:
    import constants
    # development in jupyter notebook
    import layout






logger = logging.getLogger(__name__)






from datetime import datetime
def update_function(self, msg=None, high_priority=False):
    '''update function for default provides time string and message
    
    This plugin is designed to display if all other plugins fail to load
    
    Args:
        self(`namespace`)
        msg(`str`): string to display
    %U'''
    if not msg:
        msg = constants.msg
    data = {
        'digit_time': datetime.now().strftime("%H:%M:%S"),
        'msg': msg,
    }
    if high_priority:
        priority = -2**15
    else:
        priority = 2**14
        
    is_updated = True
    return (is_updated, data, priority) 










# import SelfDummy
# s = SelfDummy.SelfDummy()
# update_function(s)




