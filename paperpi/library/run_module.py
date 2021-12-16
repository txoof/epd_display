#!/usr/bin/env python3
# coding: utf-8




import importlib
import inspect
from pathlib import Path
from datetime import datetime






def run_module(module_args=[]):
    def print_usage():
        print('Usage:')
        print('--run_plugin_func plugin.function [ARG1] [ARG2]')
        print('\nor for more information:\n--plugin_info plugin')
         
    if not module_args:
        print_usage()
        return
    
    my_module = module_args[0].split('.')
    my_args = module_args[1:]
    if len(my_args) < 1:
        my_args.append(None)
        
    if len(my_module) < 2:
        print_usage()
        return
    
    try:
        i = importlib.import_module(f'plugins.{my_module[0]}.{my_module[0]}')
    except Exception as e:
        print(type(e))
        print(f'error running plugin function: {my_module[0]}')
        return
    
    try:
        my_function = getattr(i, my_module[1])
    except AttributeError as e:
        print(f'error: module {my_module[0]} has no function "{my_module[1]}"')
        return
        
    try:
        my_function(my_args[0])
    except Exception as e:
        print(f'error: {e}')
        return
    






def add_config(module=None, config_file=None):
    def print_usage():
        print('Adds basic configuration to config file')
        print('Usage:')
        print('--add_config plugin user|daemon')
        print('\nExample: --add_config moon_phase daemon')
        print('\nfor list of plugins:\n--list_plugins')
    
    def time_stamp():
        return datetime.now().strftime('# {} added >>>>>>  %Y.%m.%d %H:%M:%S\n')    
    
    if not module:
        print_usage()
        return
    
    my_module = module
    my_config = Path(config_file)
    
    try:
        i = importlib.import_module(f'plugins.{module}.constants')
    except Exception as e:
        print(f'plugin "{module}" not found\n')
        print_usage()
        return
    
    try:
        config = i.sample_config
    except AttributeError:
        print('this plugin does not appear to have a sample configuration')
        print('aborting')
        return

    try:
        with open(config_file, 'a') as f:
            f.write(time_stamp().format('start'))
            f.write(config)
            f.write(time_stamp().format('end'))
    except PermissionError:
        print('It appears you are trying to append to the daemon config file;')
        print('you may need to run this with "sudo."')
        return
    except OSError as e:
        print(f'An error occured while writing file "{config}": {e}')
        return

    print(f'Finished writing configuration for {module}')
    print(f'It is a very good idea to open {config_file}\nand check the configuration you have just added!')
    
    




