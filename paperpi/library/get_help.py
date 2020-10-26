#!/usr/bin/env python3
# coding: utf-8




# import plugins.lms_client






import importlib
import inspect
from pathlib import Path






def get_help(module=None):
    '''display information for a plugin module including:
        Functions available
        Layouts defined
        data keys returned by update_function()
        
    Args:
        module(`str`): "plugin_name" or "plugin_name.function" or None for a list of plugins
        when a function is provided, the function is executed'''
   

    if not module:
        p = Path("./plugins/").resolve()
        print('Usage: $ paperpi -m PLUGIN_NAME|PLUGIN_NAME.FUNCTION')
        print('PLUGINS AVAILABLE:')
        for i in p.glob('*'):
            if i.is_dir() and i.name[0] not in ('_', '.'):
                print(f'  {i.name}')
        return
    
    my_module = module.split('.')
    layout_ignore = ['os', 'dir_path']
    
    
    try:
        i = importlib.import_module(f'plugins.{my_module[0]}.{my_module[0]}')
    except Exception as e:
        print(type(e))
        print(f'error gathering information for module {e}')
        return 
        
    try:
        version = i.constants.version
    except AttributeError:
        version = 'no version provided'
        
    try:
        data = i.constants.data
    except AttributeError:
        data = {'no keys available': None}
        
    
    
    if len(my_module) == 1:
        print(f'PLUGIN: {my_module[0]} v:{version}\n')
        members = inspect.getmembers(i)
        for member in members:
            if inspect.isfunction(member[1]):
                print(f'FUNCTION: {my_module[0]}.{member[0]}')
                print(member[1].__doc__,'\n')
        try:
            my_dir = dir(getattr(i, 'layout'))
        except AttributeError:
            my_dir =[f'NO LAYOUTS FOUND IN "{my_module[0]}"']
        
        print('\nLAYOUTS AVAILABLE:')
        for item in my_dir:
            if not item.startswith('__') and not item in layout_ignore:
                print(f'  {item}')
        
        print(f'\nDATA KEYS AVAILABLE FOR LAYOUTS IN {my_module[0]}:')
        for k in data.keys():
            print(f'   {k}')
        
        
    elif len(my_module) > 1:
        try:
            function = getattr(i, f'{my_module[1]}')
        except AttributeError as e:
            print(e)
            return
        print('Docstring:')
        print(function.__doc__)
        try:
            r = function()
            print('Function return value: ')
            print(r)
        except Exception as e:
            print(e)
    else:
        pass
    











