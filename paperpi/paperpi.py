#!/usr/bin/env python3
# coding: utf-8






import os
import logging 
import logging.config
import shutil
import sys
from itertools import cycle
from inspect import getfullargspec
from importlib import import_module
from time import sleep
from pathlib import Path
from distutils.util import strtobool
import waveshare_epd






import ArgConfigParse
from epdlib import Screen
from epdlib.Screen import Update
from library.CacheFiles import CacheFiles
from library.Plugin import Plugin
from library.InterruptHandler import InterruptHandler
from library import get_help
from library import run_module
import constants






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






def clean_up(cache=None, screen=None):
    logging.info('cleaning up cache and screen')
    try:
        cache.cleanup()
    except AttributeError:
        logging.debug('no cache passed, skipping')
    try:
#         screen.initEPD()
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
    
    cmd_args.add_argument('-R', '--max_refresh', required=False, default=3, 
                          dest='main__max_refresh',
                          help='maximum number of refreshes between complete screen refresh')    
    
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
    
    config_exists = True
    
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
            config_exists = False
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
    
    if not config_exists:
        msg = f'''This appears to be the first time PaperPi has been run.
A user configuration file created: {constants.config_user}
At minimum you edit this file and add a display_type
        
Edit the configu file with "$ nano {constants.config_user}"'''
        do_exit(0, msg)
    
    logging.debug(f'using configuration files to configure PaperPi: {config_files_list}')
    config_files = ArgConfigParse.ConfigFile(config_files_list, ignore_missing=True)
    config_files.parse_config()

                    
    
    return config_files






# def sanitize_vals(config):
#     '''attempt to convert all the strings into appropriate formats
#         integer/float like strings ('7', '100', '-1.3') -> int
#         boolean like strings (yes, no, Y, t, f, on, off) -> 0 or 1
#     Args:
#         config(`dict`): nested config.ini style dictionary
    
#     Returns:
#         `dict`'''
    
#     def convert(d, func, exceptions):
#         '''convert values in nested dictionary using a specified function
#             values that raise an exception are left unchanged
        
#         Args:
#             d(`dict`): nested dictionary {'Section': {'key': 'value'}}
#             func(`function`): function such as int() or strtobool()
#             exceptions(`tuple`): 
            
#         Returns:
#             `dict`'''
#         for section, values in d.items():
#             for key, value in values.items():
#                 if isinstance(value, str):
#                     try:
#                         sanitized = func(value)
#                     except exceptions:
#                         sanitized = value
#                     d[section][key] = sanitized
#         return d
    
#     #attempt to convert any string that looks like int into the proper value
#     # convert strings to float if possible
#     str_to_float = convert(config, float, (ValueError))
#     str_to_ints = convert(str_to_float, int, (ValueError))
#     # attempt to convert any string that looks like a bool into a bool
#     str_to_bool = convert(str_to_ints, strtobool, (ValueError, AttributeError))
    
#     config = str_to_bool
    
    
        
#     return config






def sanitize_vals(config):
    '''attempt to convert all the strings into appropriate formats
             integer/float like strings ('7', '100', '-1.3') -> int or float
             boolean like strings (yes, no, Y, t, f, on, off) -> 0 or 1
         Args:
             config(`dict`): nested config.ini style dictionary

         Returns:
             `dict`'''    
    def strtofloat(s):
        '''strings to float if possible'''
        retval = s
        if isinstance(s, str):
            if '.' in s:
                try:
                    retval = float(s)
                except ValueError:
                    pass

        return retval

    def convert(d, new_type, exceptions):
        for section, values in d.items():
            for key, value in values.items():
                if isinstance(value, str):
                    try:
                        sanitized = new_type(value)
                    except exceptions:
                        sanitized = value

                    d[section][key] = sanitized
                else:
                    d[section][key] = value
        return d

    convert(config, strtofloat, ValueError)
    convert(config, int, (ValueError))
    convert(config, strtobool, (ValueError, AttributeError))
    
    return config






def setup_splash(config, resolution):
    logging.debug('checking splash settings')
    if 'splash' in config['main']:
        logging.debug('checking splash screen settings')
        if config['main']['splash']:
            logging.debug('splash enabled in confg file')
            splash = True
        else:
            logging.debug('splash disabled in config file')
            splash = False
    else:
        splash = True

    if splash:
        logging.debug('splash screen enabled')
        from plugins.splash_screen import splash_screen
        splash_config = { 
            'name': 'Splash Screen',
            'layout': splash_screen.layout.layout,
            'update_function': splash_screen.update_function,
            'resolution': resolution
        } 
        logging.debug(f'configuring splash screen: {splash_config}')
        splash = Plugin(**splash_config)
        splash.update(constants.app_name, constants.version, constants.url)
        logging.debug(f'splash screen image type: {type(splash.image)}')
    return splash






def setup_display(config):
    def ret_obj(obj=None, status=0, message=None):
        return{'obj': obj, 'status': status, 'message': message}    
    keyError_fmt = 'configuration KeyError: section[{}], key: {}'

    moduleNotFoundError_fmt = 'could not load module: {} -- error: {}'
    
#     try:
#         logging.debug('setting display type')
#         epd_module = '.'.join([constants.waveshare_epd, config['main']['display_type']])
#         epd = import_module(epd_module)
#     except KeyError as e:
#         return_val = ret_obj(obj=None, status=1, message=keyError_fmt.format('main', 'display_type'))
#         logging.error(return_val['message'])
#         return return_val
#     except ModuleNotFoundError as e:
#         logging.error('Check your config files and ensure a known waveshare_epd display is specified!')
#         return_val = ret_obj(None, 1, moduleNotFoundError_fmt.format(config["main"]["display_type"], e))
#         return return_val
#     except FileNotFoundError as e:
#         msg = f''''Error loading waveshare_epd module: {e}
#         This is typically due to SPI not being enabled, or the current user is 
#         not a member of the SPI group.
#         "$ sudo raspi-config nonint get_spi" will return 0 if SPI is enabled
#         Try enabling SPI and run this program again. '''
#         logging.error(msg)
#         return_val = ret_obj(obj=None, status=1, message=msg)
#         return return_val
    
    epd = config['main']['display_type']
    vcom = config['main']['vcom']
    screen = Screen(epd=epd, vcom=vcom)
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
        logging.info(keyError_fmt.format('main', 'rotation'))
        logging.info('using default: 0')
    try:
        screen.rotation = config['main']['rotation']
    except ValueError as e:
        logging.error('invalid rotation; valid values are: 0, 90, -90, 180')
        return_val = ret_obj(None, 1, keyError_fmt.format('main', 'rotation'))
        
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
            except ModuleNotFoundError as e:
                logging.warning(f'error: {e} while loading module {constants.plugins}.{values["plugin"]}')
                logging.warning(f'skipping module')
                continue
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
        try:
            module = import_module(f'{constants.plugins}.default')
        except ModuleNotFoundError as e:
            msg = f'could not load {constants.plugins}.default'
            logging.error(msg)
            do_exit(1, msg)
        my_config['update_function'] = module.update_function
        my_config['layout'] = getattr(module.layout, 'default')
        my_plugin = Plugin(**my_config)
        plugins.append(my_plugin)
        
    return plugins






def update_loop(plugins, screen, max_refresh=2):
    exit_code = 1
    logging.info('starting update loop')
    
    
    def update_plugins(): 
        '''run through all active plugins and update while recording the priority'''
        my_list = []
        logging.info('*'*15)
        logging.info(f'My PID: {os.getppid()}')
        logging.info(f'updating {len(plugins)} plugins')
        for plugin in plugins:
            plugin.update()
            logging.debug(f'update: [{plugin.name}]-p: {plugin.priority}')
            my_list.append(plugin.priority)
        logging.debug(f'priorities: {my_list}')
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
    
    # count the number of refreshes for HD Screens
    refresh_count = 0    
    
    logging.info(f'max_priority: {max_priority}')
    
    
    
    for plugin in plugins:
        if plugin.priority <= max_priority:
            this_hash = plugin.hash
            logging.info(f'**** displaying {plugin.name} ****')
#             screen.initEPD()
            screen.writeEPD(plugin.image)
            break
    
    

    
    with InterruptHandler() as h:
        while True:    
            if h.interrupted:
                logging.info('caught interrupt -- stoping execution')
                exit_code = 0
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
#                     screen.initEPD()
                    logging.debug(f'image type: {type(this_plugin.image)}')
    
                    # wipe screen if the max_refresh count is exceeded
                    if refresh_count > max_refresh:
                        refresh_count = 0
                        if screen.HD:
                            logging.info('max_refresh exceeded, wiping screen prior to next update')
                            screen.clearEPD()
                        else:
                            logging.debug(f'{max_refresh - refresh_count} refreshes remain before full wipe')
                    
                    logging.debug('writing image to screen')
                    screen.writeEPD(this_plugin.image)
                    refresh_count += 1
#                     if screen.writeEPD(this_plugin.image):
#                         logging.debug('successfully wrote image')
#                         refresh_count += 1
#                     else:
#                         logging.warning('#=#=# failed to write image #=#=#')
#                         logging.info('trying next plugin')
#                         plugin_is_active = False
                        
                    
                else:
                    logging.debug('plugin data not refreshed -- skipping screen refresh')
                this_plugin_timer.update()    
                    
        
            sleep(1)
    return exit_code






def main():
    
    # change the working directory -- this simplifies all path work later on
    os.chdir(constants.absolute_path)
    
    # set the absolute path to the current directory
    absolute_path = constants.absolute_path
       
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
        print(get_help.get_help(cmd_args.options.plugin_info))
        return
    
    if cmd_args.options.list_plugins:
        print(get_help.get_help())
        return
    
    if cmd_args.options.run_plugin_func:
        run_module.run_module(cmd_args.options.run_plugin_func)
        return
    
    # make sure all the integer-like strings are converted into integers
    config = sanitize_vals(config)
#     return config
    
    
    logger.setLevel(config['main']['log_level'])
    logging.root.setLevel(config['main']['log_level'])
    
    logging.debug(f'********** PaperPi {constants.version} Starting **********')
    
    # configure screen
    screen_return = setup_display(config)
    if screen_return['obj']:
        screen = screen_return['obj']
    else:
        clean_up(None, None)
        logging.error(f'config files used: {config_files.config_files}')
        do_exit(**screen_return)
    
    # try to set up the splash screen several times here -- this may solve the None image problem.
    splash = setup_splash(config, screen.resolution)
    
    if splash:
        
        logging.debug('displaying splash screen')
        logging.debug(f'image type: {type(splash.image)}')
        screen.writeEPD(splash.image)
        
    
    cache = CacheFiles(path_prefix=constants.app_name)
    plugins = build_plugin_list(config, screen.resolution, cache)
    
    exit_code = update_loop(plugins, screen)

    logging.info('caught terminate signal -- cleaning up and exiting')
    clean_up(cache, screen)
    
    return exit_code






if __name__ == "__main__":
    # remove jupyter runtime junk for testing
    if len(sys.argv) >= 2 and 'ipykernel' in sys.argv[0]:
        sys.argv = [sys.argv[0]]
        sys.argv.extend(sys.argv[3:])
    exit_code = main()
    sys.exit(exit_code)








# logger = logging.getLogger(__name__)
# logger.root.setLevel('DEBUG')


