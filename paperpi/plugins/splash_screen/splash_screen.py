#!/usr/bin/env python3
# coding: utf-8




try:
    from . import layout
#     from . import constants_spot
except ImportError:
    import layout
#     import constants_spot






def update_function(self, app_name, version, url):
    return(True, {'app_name': app_name, 'version': version, 'url': url}, -1)











