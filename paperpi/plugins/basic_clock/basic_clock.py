#!/usr/bin/env python3
# coding: utf-8




import logging






# two different import modes for development or distribution
try:
    # import from other modules above this level
    from . import layout
    from . import constants
except ImportError:
    # development in jupyter notebook
    import layout
    import constants






logger = logging.getLogger(__name__)






from datetime import datetime
def update_function(self):
    '''provides system time string in the format HH:MM
    
    Args:
        None
    

    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))
    %U'''
    data = {'digit_time': datetime.now().strftime("%H:%M")}
    priority = self.max_priority
    is_updated = True
    
    return (is_updated, data, priority) 










# import SelfDummy
# s = SelfDummy.SelfDummy()
# update_function(s)




