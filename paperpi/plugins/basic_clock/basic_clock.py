#!/usr/bin/env python3
# coding: utf-8




import logging






# two different import modes for development or distribution
try:
    # import from other modules above this level
    from . import layout
    from . import my_help
except ImportError:
    # development in jupyter notebook
    import layout
    import my_help






logger = logging.getLogger(__name__)






from datetime import datetime
def update_function(self):
    data = {'digit_time': datetime.now().strftime("%H:%M")}
    priority = self.max_priority
    is_updated = True
    
    return (is_updated, data, priority) 










# import SelfDummy
# s = SelfDummy.SelfDummy()
# update_function(s)




