#!/usr/bin/env python3
# coding: utf-8








import logging
import logging.config
import shutil
import sys
from itertools import cycle
from inspect import getfullargspec
from importlib import import_module
from time import sleep
from pathlib import Path
from os import chdir
from distutils.util import strtobool






import ArgConfigParse
from epdlib import Screen
from epdlib.Screen import Update
from library.CacheFiles import CacheFiles
from library.Plugin import Plugin
from library.InterruptHandler import InterruptHandler
from library import get_help
from library import run_module
import constants
import errors






def do_exit(status=0, message=None, **kwargs):
    if message:
        if status > 0:
            logging.error(f'failure caused exit: {message}')
        border = '\n'+'#'*70 + '\n'
        message = border + message + border + '\n***Exiting***'
        print(message)
        
    try:
        sys.exit(status)
    except Exception as e:
        pass






def ret_obj(obj=None, status=0, message=None):
    return{'obj': obj, 'status': status, 'message': message}






def clean_up(cache=None, screen=None):
    logging.info('cleaning up cache and screen')
    try:
        cache.cleanup()
    except AttributeError:
        logging.debug('no cache passed, skipping')
    try:
        screen.initEPD()
        screen.clearEPD()
    except AttributeError:
        logging.debug('no screen passed, skipping')
    return






def get_cmd_line_args():
    cmd_args = ArgConfigParse.CmdArgs()
    cmd_args.add_argument('-c', '--config', ignore_none=True, metavar='CONFIG_FILE.ini',
                         type=str, dest='user_config',
                         help='use the specified configuration file')
    
    cmd_args.add_argument('-l', '--log_level', ignore_none=True, metavar='LOG_LEVEL',
                         type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                         dest='main__log_level', help='change the log output level')
    
    cmd_args.add_argument('--plugin_info', metavar='[plugin|plugin.function]',
                         required=False, default=None,
                         ignore_none=True,
                         help='get information for plugins and user-facing functions provided by a plugin')
    
    cmd_args.add_argument('--list_plugins', required=False,
                         default=False, action='store_true', 
                         help='list all available plugins')
    
    cmd_args.add_argument('--run_plugin_func',
                         required=False, default=None, nargs='+',
                         metavar=('plugin.function', 'optional_arg1 arg2 argN'),
                         ignore_none=True,
                         help='run a user-facing function for a plugin')
    
    cmd_args.add_argument('-d', '--daemon', required=False, default=False,
                         dest='main__daemon', action='store_true', 
                         help='run in daemon mode (ignore user configuration if found)')
    
    cmd_args.add_argument('-V', '--version', required=False, default=False, ignore_false=True,
                          action='store_true',
                          help='display version and exit')
    
   
    cmd_args.parse_args()    
 
    return cmd_args






def get_config_files(cmd_args):
    '''read config.ini style file(s)
    Args:
        cmd_args(`ArgConfigParse.CmdArgs()` object)
    
    Returns:
        `ArgConfigParse.ConfigFile`'''
    config_files_list = [constants.config_base, constants.config_system, constants.config_user]
    
    daemon = False
    
    if hasattr(cmd_args.options, "main__daemon"):
        logging.debug('-d specified on command line')
        if cmd_args.options.main__daemon:
            logging.debug('excluding user config files')
            config_files_list.pop()
            daemon = True
        else:
            daemon = False
    else: 
        daemon = False
    
    if not daemon:
        # create a user config directory
        if not constants.config_user.exists():
            logging.info('creating user config directory and inserting config file')
            try:
                constants.config_user.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError as e:
                logging.warning(f'could not create {constants.config_user}: {e}')
        if not constants.config_user.exists():
            try:
                shutil.copy(constants.config_base, constants.config_user)
            except Exception as e:
                logging.critical(f'could not copy configuration file to {constants.config_user}: {e}')

    config_files = ArgConfigParse.ConfigFile(config_files_list, ignore_missing=True)
    config_files.parse_config()

                    
    
    return config_files






def sanitize_vals(config):
    '''attempt to convert all the strings into appropriate formats
        integer/float like strings ('7', '100', '-1.3') -> int
        boolean like strings (yes, no, Y, t, f, on, off) -> 0 or 1
    Args:
        config(`dict`): nested config.ini style dictionary
    
    Returns:
        `dict`'''
    
    def convert(d, func, exceptions):
        '''convert values in nested dictionary using a specified function
            values that raise an exception are left unchanged
        
        Args:
            d(`dict`): nested dictionary {'Section': {'key': 'value'}}
            func(`function`): function such as int() or strtobool()
            exceptions(`tuple`): 
            
        Returns:
            `dict`'''
        for section, values in d.items():
            for key, value in values.items():
                try:
                    sanitized = func(value)
                except exceptions:
                    sanitized = value
                d[section][key] = sanitized
        return d
    
    #attempt to convert any string that looks like an int/float into a string
    str_to_ints = convert(config, int, (ValueError))
    # attempt to convert any string that looks like a bool into a bool
    str_to_bool = convert(str_to_ints, strtobool, (ValueError, AttributeError))
    
    config = str_to_bool
    
    
        
    return config






def setup_splash(config, resolution):
    logging.debug('checking splash settings')
    if 'splash' in config['main']:
        logging.debug('checking splash screen settings')
        if config['main']['splash']:
            splash = True
        else:
            logging
            splash = False
    else:
        splash = True

    if splash:
        from plugins.splash_screen import splash_screen
        splash_config = { 
            'name': 'Splash Screen',
            'layout': splash_screen.layout.layout,
            'update_function': splash_screen.update_function,
            'resolution': resolution
        } 
        logging.debug('configuring and displaying splash screen')
        splash = Plugin(**splash_config)
        splash.update(constants.app_name, constants.version, constants.url)    
    return splash






def setup_display(config):
    try:
        logging.debug('setting display type')
        epd_module = '.'.join([constants.waveshare_epd, config['main']['display_type']])
        epd = import_module(epd_module)
    except KeyError as e:
        return_val = ret_obj(obj=None, status=1, message=errors.keyError_fmt.format('main', 'display_type'))
        logging.error(return_val['message'])
        return return_val
    except ModuleNotFoundError as e:
        logging.error('Check your config files and ensure a known waveshare_epd display is specified!')
        return_val = ret_obj(None, 1, errors.moduleNotFoundError_fmt.format(config["main"]["display_type"], e))
        return return_val
        
    screen = Screen()
    try:
        screen.epd = epd
    except PermissionError as e:
        logging.critical(f'Error initializing EPD: {e}')
        logging.critical(f'The user executing {constants.app_name} does not have access to the SPI device.')
        return_val = ret_obj(None, 1, 'This user does not have access to the SPI group\nThis can typically be resolved by running:\n$ sudo groupadd <username> spi')
        return return_val

    try:
        config['main']['rotation'] = int(config['main']['rotation'])
    except KeyError as e:
        logging.info(errors.keyError_fmt.format('main', 'rotation'))
        logging.info('using default: 0')
    try:
        screen.rotation = config['main']['rotation']
    except ValueError as e:
        logging.error('invalid rotation; valid values are: 0, 90, -90, 180')
        return_val = ret_obj(None, 1, errors.keyError_fmt.format('main', 'rotation'))
        
    return ret_obj(obj=screen)






def build_plugin_list(config, resolution, cache):
    # get the expected key-word args from the Plugin() spec
    spec_kwargs = getfullargspec(Plugin).args

    plugins = []

    for section, values in config.items():
        # ignore the other sections
        if section.startswith('Plugin:'):
            logging.info(f'[[ {section} ]]')

            my_config = {}
            # add all the spec_kwargs from the config
            plugin_kwargs = {}
            for key, val in values.items():
                if key in spec_kwargs:
                    my_config[key] = val
                else:
                    # add everything that is not one of the spec_kwargs to this dict
                    plugin_kwargs[key] = val

            # populate the kwargs my_config dict that will be passed to the Plugin() object
            my_config['name'] = section
            my_config['resolution'] = resolution
            my_config['config'] = plugin_kwargs
            my_config['cache'] = cache
            try:
                module = import_module(f'{constants.plugins}.{values["plugin"]}')
                my_config['update_function'] = module.update_function
                my_config['layout'] = getattr(module.layout, values['layout'])
            except KeyError as e:
                logging.info('no module specified; skipping update_function and layout')
            my_plugin = Plugin(**my_config)
            try:
                my_plugin.update()
            except AttributeError as e:
                logging.warning(f'ignoring plugin {my_plugin.name} due to missing update_function')
                logging.warning(f'plugin threw error: {e}')
                continue
            logging.info(f'appending plugin {my_plugin.name}')
            plugins.append(my_plugin)
            
            
    if len(plugins) < 1:
        my_config = {}
        logging.warning('no plugins were loaded! falling back to default plugin.')
        my_config['name'] = 'default plugin'
        my_config['resolution'] = resolution
        my_config['cache'] = cache
        module = import_module(f'{constants.plugins}.default')
        my_config['update_function'] = module.update_function
        my_config['layout'] = getattr(module.layout, 'default')
        my_plugin = Plugin(**my_config)
        plugins.append(my_plugin)
        
    return plugins






def update_loop(plugins, screen):
    logging.info('starting update loop')
    
    
    def update_plugins(): 
        '''run through all active plugins and update while recording the priority'''
        my_list = []
        logging.info('*'*15)
        logging.info(f'updating {len(plugins)} plugins')
        for plugin in plugins:
            plugin.update()
            logging.info(f'update: [{plugin.name}]-p: {plugin.priority}')
            my_list.append(plugin.priority)
        logging.info(f'priorities: {my_list}')
        return my_list
        
    # use itertools cycle to move between list elements
    plugin_cycle = cycle(plugins)
    plugin_is_active = False
    # current plugin for display
    this_plugin = next(plugin_cycle)
    # track time plugin is displayed for
    this_plugin_timer = Update()
    # each plugin generates a unique hash whenever it is updated
    this_hash = ''
    
    # update all the plugins and record priority
    priority_list = update_plugins()
    # this var name is confusing -- it's actually the lowest number to indicate **maximum** priority
    max_priority = min(priority_list)
    # record for comparison
    last_priority = max_priority
    
    logging.info(f'max_priority: {max_priority}')
    

    for plugin in plugins:
        if plugin.priority <= max_priority:
            this_hash = plugin.hash
            logging.info(f'**** displaying {plugin.name} ****')
            screen.initEPD()
            screen.writeEPD(plugin.image)
            break
    
    with InterruptHandler() as h:
        while True:    
            if h.interrupted:
                logging.info('caught interrupt -- stoping execution')
                break
            priority_list = update_plugins()

            # priority increases as it gets lower; 0 is considered the bottom,
            # but some modules may temporarily have a negative priority to indicate a critical
            # update 
            last_priority = max_priority
            max_priority = min(priority_list)
            
            logging.debug(f'{this_plugin.name}: last updated: {this_plugin_timer.last_updated}, min_display_time: {this_plugin.min_display_time}')
            
            
            # if the timer has expired OR a module has changed the priority setting begin the update procedure
            if this_plugin_timer.last_updated > this_plugin.min_display_time or max_priority < last_priority:
                logging.info(f'plugin expired -- switching plugin')
                plugin_is_active = False
                
                # cycle through plugins, looking for the next plugin that has high priority
                while not plugin_is_active:
                    this_plugin = next(plugin_cycle)
                    logging.debug(f'checking priority of {plugin.name}')
                    if this_plugin.priority <= max_priority:
                        plugin_is_active = True
                    else:
                        logging.debug('trying next plugin')
                        pluggin_is_active = False
                        
                logging.info(f'displaying {this_plugin.name} -- priority: {this_plugin.priority}/{max_priority}')
                
                if this_hash != this_plugin.hash:
                    logging.debug('data refreshed, refreshing screen')
                    this_hash = this_plugin.hash
                    screen.initEPD()
                    screen.writeEPD(this_plugin.image)
                    
                else:
                    logging.debug('plugin data not refreshed -- skipping screen refresh')
                this_plugin_timer.update()    
                    
        
            sleep(1)    






def main():
    # set the absolute path to the current directory
    absolute_path = constants.absolute_path
    
    # change directory into the current working directory
    # to simplify futher path related work
    chdir(absolute_path)
    
    # set up logging
    logging.config.fileConfig(constants.logging_config)
    logger = logging.getLogger(__name__)
    
    # get command line and config file arguments
    cmd_args = get_cmd_line_args()
    
    if hasattr(cmd_args, 'unknown'):
        print(f'Unknown arguments: {cmd_args.unknown}\n\n')
        cmd_args.parser.print_help()
        return
        
    
    config_files = get_config_files(cmd_args)
    
    # merge file and commandline (right-most over-writes left)
    config = ArgConfigParse.merge_dict(config_files.config_dict, cmd_args.nested_opts_dict)
    
    if cmd_args.options.version:
        print(constants.version_string)
        return
    
    if cmd_args.options.plugin_info:
        get_help.get_help(cmd_args.options.plugin_info)
        return
    
    if cmd_args.options.list_plugins:
        print(get_help.get_help())
        return
    
    if cmd_args.options.run_plugin_func:
        run_module.run_module(cmd_args.options.run_plugin_func)
        return
    
    # make sure all the integer-like strings are converted into integers
    config = sanitize_vals(config)
    
    logger.setLevel(config['main']['log_level'])
    logging.root.setLevel(config['main']['log_level'])
    
    # configure screen
    screen_return = setup_display(config)
    if screen_return['obj']:
        screen = screen_return['obj']
    else:
        clean_up(None, None)
        logging.error(f'config files used: {config_files.config_files}')
        do_exit(**screen_return)
        
    splash = setup_splash(config, screen.resolution)    
    screen.initEPD()

    if splash:
        screen.writeEPD(splash.image)
        
    
    cache = CacheFiles(path_prefix=constants.app_name)
    plugins = build_plugin_list(config, screen.resolution, cache)
    
    update_loop(plugins, screen)

    logging.info('caught terminate signal -- cleaning up and exiting')
    clean_up(cache, screen)
    return plugins






if __name__ == "__main__":
    # remove jupyter runtime junk for testing
#     if len(sys.argv) >= 2 and 'ipykernel' in sys.argv[0]:
#         sys.argv = [sys.argv[0]]
#         sys.argv.extend(sys.argv[3:])
    c = main()








# import importlib
# import inspect
# from pathlib import Path

# def run_module(module_args=[]):
#     def print_usage():
#         print('Usage:')
#         print('-r plugin.function [ARG1] [ARG2]')
#         print('\nor for more information:\n-m plugin')
        
#     if not module_args:
#         print_usage()
#         return
    
#     my_module = module_args[0].split('.')
#     my_args = module_args[1:]
        
#     if len(my_module) < 2:
#         print_usage()
#         return
    
#     try:
#         i = importlib.import_module(f'plugins.{my_module[0]}.{my_module[0]}')
#     except Exception as e:
#         print(type(e))
#         print(f'error running plugin function: {my_module[0]}')
#         return
    
#     try:
#         my_function = getattr(i, my_module[1])
#     except AttributeError as e:
#         print(f'error: module {my_module[0]} has no function "{my_module[1]}"')
#         return
        
#     try:
#         my_function(my_args[0])
#     except Exception as e:
#         print(f'error: {e}')
#         return
    
        






# a.options.run_module

# # run_module(['met_no']) #, 'Denver, Colorado USA'])
# q = run_module(['met_no.get_coord', 'Maroon Bells, Colorado USA', 7, 'cow'])

# run_module(['lms_client.scan_servers', 'abc', {'place': 7}])

# get_help.get_help()

# q.get_coord

# f = getattr(q, 'xget_coord')

# f("Golden Colorado USA")






# import importlib
# import inspect
# from pathlib import Path

# def nget_help(module=None):
#     '''display information for a plugin module including:
#         Functions available
#         Layouts defined
#         data keys returned by update_function()
        
#     Args:
#         module(`str`): "plugin_name" or "plugin_name.function" or None for a list of plugins
#         when a function is provided, the function is executed'''
   

#     if not module:
#         p = Path("./plugins/").resolve()
#         print('Usage: $ paperpi -m PLUGIN_NAME|PLUGIN_NAME.FUNCTION')
#         print('PLUGINS AVAILABLE:')
#         for i in p.glob('*'):
#             if i.is_dir() and i.name[0] not in ('_', '.'):
#                 print(f'  {i.name}')
#         return
    
#     my_module = module.split('.')
#     layout_ignore = ['os', 'dir_path']
    
    
#     try:
#         i = importlib.import_module(f'plugins.{my_module[0]}.{my_module[0]}')
#     except Exception as e:
#         print(type(e))
#         print(f'error gathering information for module {e}')
#         return 
        
#     try:
#         version = i.constants.version
#     except AttributeError:
#         version = 'no version provided'
        
#     try:
#         data = i.constants.data
#     except AttributeError:
#         data = {'no keys available': None}
        
    
    
#     if len(my_module) == 1:
#         print(f'PLUGIN: {my_module[0]} v:{version}\n')
#         members = inspect.getmembers(i)
#         for member in members:
#             if inspect.isfunction(member[1]):
#                 # skip entries that don't have a docstring
#                 if not member[1].__doc__:
#                     continue
#                 # skip docstrings functions not tagged with '%U' as last characters
#                 if member[1].__doc__.endswith('%U'):
#                     print(f'FUNCTION: {my_module[0]}.{member[0]}')
#                     print(member[1].__doc__.replace('%U', ''))
#                     print('_'*75)
#                 else:
#                     continue
#         try:
#             my_dir = dir(getattr(i, 'layout'))
#         except AttributeError:
#             my_dir =[f'NO LAYOUTS FOUND IN "{my_module[0]}"']
        
#         print('LAYOUTS AVAILABLE:')
#         for item in my_dir:
#             if not item.startswith('__') and not item in layout_ignore:
#                 print(f'  {item}')
        
#         print(f'\nDATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY {my_module[0]}:')
#         for k in data.keys():
#             print(f'   {k}')
        
        
#     elif len(my_module) > 1:
#         try:
#             function = getattr(i, f'{my_module[1]}')
#         except AttributeError as e:
#             print(e)
#             return
#         print('Docstring:')
#         print(function.__doc__)
#         try:
#             r = function()
#             print('Function return value: ')
#             print(r)
#         except Exception as e:
#             print(e)
#     else:
#         pass
    









