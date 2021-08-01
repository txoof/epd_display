#!/usr/bin/env python3
# coding: utf-8






import logging
import hashlib
import time
from epdlib import Layout






logger = logging.getLogger(__name__)






def strict_enforce(*types):
    """strictly enforce type compliance within classes
    
    Usage:
        @strict_enforce(type1, type2, (type3, type4))
        def foo(val1, val2, val3):
            ...
    """
    def decorator(f):
        def new_f(self, *args, **kwds):
            #we need to convert args into something mutable   
            newargs = []        
            for (a, t) in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f'"{a}" is not type {t}')
#                 newargs.append( t(a)) #feel free to have more elaborated convertion
            return f(self, *args, **kwds)
        return new_f
    return decorator






class Plugin:
    '''Plugin class for creating and managing plugins'''
    def __init__(self, resolution, name=None, 
                 layout={}, 
                 update_function=None, 
                 max_priority=2**15,
                 refresh_rate=60, 
                 min_display_time=30, 
                 config={},
                 cache=None,
                 **kwargs):
        '''Create a plugin object that provides consistent methods for providing an image and querying
        various services
        
        Properties:
            hash('str'): unique identifier for this plugin in its current state (used for checking for changes)
            image(PIL image): image generated for this plugin
            data(dict): data returned by this plugin to be used in the Layout
            priority(int): current priority for this plugin (lower numbers are more important in display loop)
            last_ask(float): time in seconds since this plugin was last asked for an update -- used for throttling
        
        Args:
            resolution(`tuple` of `int`): resolution of the epd or similar screen: (Length, Width)
            name(`str`): human readable name of the function for logging and reference
            layout(`dict`): epdlib.Layout.layout dictionary that describes screen layout
            update_function(func): function that returns plugin status, data and priority a
                update_function must accept (self, *args, **kwargs) and must return
                a tuple of (is_updated(bool), data(dict), priority(int))
            max_priority(`int`): maximum priority for this module values approaching 0 have highest
                priority, values < 0 are inactive
            refresh_rate(`int`): minimum time in seconds between requests for pulling an update
            min_display_time(`int`): minimum time in seconds plugin should be allowed to display in the loop
            config(`dict`): any kwargs that update function requires
            cache(`CacheFiles` obj): object that can be used for downloading remote files and caching
            kwargs(): any additional kwargs will be ignored
            '''
        self.name = name
        if resolution:
            self.resolution = resolution
        
        self.layout = layout
        
#         if update_function:
#             self._add_update_function(update_function)
#         else:
# #             self.update_function = print('no update function set')
#             pass
        self.update_function = update_function
    
        self.max_priority = max_priority
        
        self.refresh_rate = refresh_rate
        self.min_display_time = min_display_time
        
        self.config = config

        self.cache = cache
        
        self._last_ask = 0
        self.hash = self._generate_hash()
        self.data = {}
        self.image = None
        self.priority = max_priority
    
    @property
    def name(self):
        '''name of plugin
        name(`str`)'''
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = str(name)
        
    @property
    def resolution(self):
        '''resolution of attached screen that will be used for output
            resolution(`tuple` of `int`)'''
        return self._resolution
        
    @resolution.setter
    @strict_enforce((list, tuple))
    def resolution(self, resolution):
        self._resolution = resolution    
    
    @property
    def layout(self):
        '''epdlib.Layout.layout dictionary used for configuring text and image blocks
            layout(`dict`)'''
        return self.layout_obj.layout
    
    @layout.setter
    @strict_enforce(dict)
    def layout(self, layout):
        self.layout_obj = Layout(resolution=self.resolution, layout=layout)
        
    
    @property
    def update_function(self):
        '''update function provided by the plugin module
        
        The update_function is called by the update method to provide status and data for 
        the Plugin.
        
        Args:
            function(function): function that accepts self, *args, **kwargs
            
        Returns:
            tuple of is_updated(bool), data(dict), priority(int)'''
        return self._update_function
    
    @update_function.setter
    def update_function(self, function):
        if not function:
            self._update_function = None
        else:
            self._update_function = function.__get__(self)
    
    @property
    def cache(self):
        '''CacheFiles object used for caching remote files used by plugins
        cache(`CacheFiles` obj)'''
        return self._cache
    
    @cache.setter
    def cache(self, cache):
        if cache:
            self._cache = cache
        else:
            self._cache = None
    
    @property
    def last_ask(self):
        '''Records monotonic time of last time an update function was called 
            This is used by the self._is_ready() function to throttle update requests'''
        return self._last_ask
    
    @last_ask.setter
    def last_ask(self, last_ask):
        self._last_ask = last_ask
        
    
#     def _add_update_function(self, function):
#         '''private function for adding update_functions properly to class'''
#         self.update_function = function.__get__(self)
        
    def _generate_hash(self):
        '''generate a hash based on the self.name and the current time
            This is updated whenever self.data is updated and can be checked as a 
            proxy for "new data"'''
        my_hash = hashlib.sha1()
        my_hash.update(str(time.time()).encode('utf-8')+str(self.name).encode('utf-8'))
        return my_hash.hexdigest()[:10]        
    
    def _is_ready(self):
        '''simple throttle of update requests
            Checks time between current request (monotonic) and self._last_ask and compares to 
            self.refresh_rate
        
        Returns:
            `bool`: True if cooldown period has expired, false otherwise'''
        if time.monotonic() - self._last_ask > self.refresh_rate:
            self._last_ask = time.monotonic()
            return True
        else:
            logging.debug(f'throttling in effect -- wait for {self.refresh_rate - (time.monotonic() - self._last_ask)} seconds before requesting update')
            return False
        
    def update(self, *args, **kwargs):
        '''request an update of the plugin data
            requests are throttled if they occur sooner than the cool-down period
            defined by self.refresh_rate
            
            Returns:
                self.hash(hash of time and self.name)
            
            calls self.update_function(*args, **kwargs):
                self.update_function returns: (`tuple` of `bool`, `dict`, `int`): 
                    bool(true when plugin is updated) 
                    dict(data returned from plugin update_function to be passed into a layout)
                    int(priority of this module; values approaching 0 are highest, negative
                        values indicate plugin is inactive)

            
            Set here:
                self.data
                self.layout_obj.update_contents(self.data)
                self.hash'''
        if self._is_ready():
            is_updated, data, priority = self.update_function(*args, **kwargs)
            if data != self.data:
                self.data = data
                self.layout_obj.update_contents(data)
                self.image = self.layout_obj.concat()
                self.hash = self._generate_hash()
            # always update the priority    
            self.priority = priority
        else:
            pass
        
            
        return self.hash
    






def main():
    '''demo of Plugin data type'''
    from random import randint
    from IPython.display import display
    from time import sleep
    bogus_layout = {
        'number': {
            'image': None,
            'max_lines': 1,
            'width': 1,
            'height': 1,
            'abs_coordinates': (0, 0),
            'rand': True,
            'font': '../fonts/Dosis/Dosis-VariableFontwght.ttf',
        },
    }

    # update_function that is added to the plugin as the method self.update_function
    def bogus_plugin(self):
        data = {'number': str(randint(99,9999))}
        priority = self.max_priority
        is_updated = True

        return (is_updated, data, priority) 


    p = Plugin(resolution=(300, 210), 
               refresh_rate=3, 
               max_priority=1, 
               update_function=bogus_plugin, 
               layout=bogus_layout)

#     Plugin.update_function = bogus_plugin
    
    logger.root.setLevel('DEBUG')
    print('this demo is best run from inside jupyter notebook')
    for i in range(5):
        print('trying to update plugin')
        p.update()
        print('displaying image')
        display(p.image)
        print('sleep for 1 second')
        sleep(1)
    return p






if __name__ == '__main__':
    p = main()









