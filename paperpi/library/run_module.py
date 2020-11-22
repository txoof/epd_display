#!/usr/bin/env python3
# coding: utf-8




import importlib
import inspect
from pathlib import Path






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




