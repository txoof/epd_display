#!/usr/bin/env python3
# coding: utf-8




import importlib
import inspect
from pathlib import Path
import textwrap






class multi_line_string():
    def __init__(self, s='', columns=65):
        self._string = []
        self.string = s
        self.columns=columns
    
    def __str__(self):
        return self.string
        
    @property
    def string(self):
        return '\n'.join(self._string)
            
    @string.setter
    def string(self, s):
        self._string.append(s)
    
    @property
    def string_list(self):
        return self._string
    
    @property
    def wrapped_string(self):
        return '\n'.join(textwrap.wrap(' '.join(self._string), self.columns)).lstrip()
    
        






def get_modules(root='./plugins/'):
    '''get a list of modules contained within the path specified
    
    Args:
        root(str): path to search for modules
    
    Returns:
        list of str: list modules found within the root'''
    module_list = []
    p = Path(root).resolve()
    for i in p.glob('*'):
        if i.is_dir() and i.name[0] not in ('_', '.'):
            module_list.append(i.name)
    return module_list






def get_module_docs(module):
    '''return only user-facing docstrings that contain "%U"
        
    Args:
        module: python module
        
    Returns:
        string containing docstrings
    '''
    mls = multi_line_string()
    members = inspect.getmembers(module)
    for member in members:
        if inspect.isfunction(member[1]):
            # skip entries that don't have a docstring
            if not member[1].__doc__:
                continue
            # skip docstrings functions not tagged with '%U' as last characters
            if member[1].__doc__.endswith('%U'):
                mls.string = f'FUNCTION: {member[0]}'
                mls.string = member[1].__doc__.replace('%U', '')
                mls.string = '_'*75
                mls.string = ' '
            else:
                continue

    return mls.string






def get_layouts(module):
    '''get layout names provided by a plugin
    
    Args:
        module: python module
        
    Returns:
        string containing layout names'''
    layout_ignore = ['os', 'dir_path']
    mls = multi_line_string()
    try:
        my_dir = dir(getattr(module, 'layout'))
    except AttributeError:
        my_dir =[f'NO LAYOUTS FOUND IN {module.__name__}']

    mls.string = 'LAYOUTS AVAILABLE:'
    for item in my_dir:
        if not item.startswith('__') and not item in layout_ignore:
            mls.string = f'  {item}'
    return mls.string






def get_data_keys(module):
    '''return data keys provided by plugin
    
    Args:
        module: python module
        
    Returns:
        string containing data keys provided by a plugin's update_function '''
    mls = multi_line_string()
    try:
        data = module.constants.data
    except AttributeError:
        data = {'no keys available': None}
    mls.string = f'\nDATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY {module.__name__}:'
    for k in data.keys():
        mls.string = f'   {k}'
    return mls.string






def get_doc_string(module, function):
    '''return a docstring for a function from within a module
        
    Args:
        module: python module
        function(str): string of function contained in module
        
    Returns:
        string containing docstring of for module.function'''
    try:
        f = getattr(module, function)
    except AttributeError as e:
        return e
    return f.__doc__






def get_help(module=None):
    '''display information for a plugin module including:
        * Functions available
        * Layouts defined
        * data keys returned by update_function()
        
    Args:
        module(`str`): "plugin_name" or "plugin_name.function" or None for a list of plugins
        when a function is provided, the function is executed'''
   
    plugin_list = []
    if not module:
        p = Path("./plugins/").resolve()
        print('get plugin information and user-facing functions:')
        print('Usage: --plugin_info PLUGIN_NAME|PLUGIN_NAME.FUNCTION')
        print('PLUGINS AVAILABLE:')
        for i in get_modules():
            print(f'  {i}')
        return
    
    my_module = module.split('.')
    
    
    try:
        i = importlib.import_module(f'plugins.{my_module[0]}.{my_module[0]}')
    except Exception as e:
        print(f'error gathering information for module {e}')
        return 
        
    try:
        version = i.constants.version
    except AttributeError:
        version = 'no version provided'
    
    if len(my_module) == 1:
        plugin_list.append(my_module)
        print(f'PLUGIN: {my_module[0]} v:{version}\n')
        print(get_module_docs(i))

        print(get_layouts(i))
        print(get_data_keys(i))
               
    elif len(my_module) > 1:
        print(get_doc_string(i, my_module[1]))
    else:
        pass











