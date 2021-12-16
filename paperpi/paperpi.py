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
from configparser import DuplicateSectionError






import ArgConfigParse
from epdlib import Screen
from epdlib.Screen import Update
from epdlib.Screen import ScreenError
from library.CacheFiles import CacheFiles
from library.Plugin import Plugin
from library.InterruptHandler import InterruptHandler
from library import get_help
from library import run_module
import my_constants as constants






def do_exit(status=0, message=None, **kwargs):
    '''exit with optional message
    Args:
        status(int): integers > 0 exit with optional message
        message(str): optional message to print'''
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
    '''clean up the screen and cache
    
    Args:
        cache(cache obj): cache object to use for cleanup up
        screen(Screen obj): screen to clear
    '''
    logging.info('cleaning up cache and screen')
    try:
        logging.debug('clearing cache')
        cache.cleanup()
    except AttributeError:
        logging.debug('no cache passed, skipping')
    try:
#         screen.initEPD()
        logging.debug('clearing screen')
        screen.clearEPD()
    except AttributeError:
        logging.debug('no screen passed, skipping')
        
    logging.debug('cleanup completed')
    return






def get_cmd_line_args():
    '''get command line arguments
    
    Returns:
        dict of parse config values'''
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
    
    cmd_args.add_argument('--add_config', 
                         required=False, default=None, nargs=2,
                         metavar=('plugin', 'user|daemon'),
                         ignore_none = True,
                         help='copy sample config to the user or daemon configuration file')
    
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
    
    cmd_args.add_argument('-R', '--max_refresh', required=False, ignore_none=True, default=None,
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
        cmd_args(`ArgConfigParse.CmdArgs` obj)
    
    Returns:
        ArgConfigParse.ConfigFile'''
    
    logging.debug('gathering configuration files')
    
    config_files_dict = {'base': constants.config_base,
                         'system': constants.config_system,
                         'user': constants.config_user,
                         'cmd_line': cmd_args.options.user_config}
    
    config_files_list = [config_files_dict['base']]
    
    if cmd_args.options.main__daemon:
        logging.debug(f'using daemon configuration: {constants.config_system}')
        config_files_list.append(config_files_dict['system'])
    else:
        if constants.config_user.exists():
            config_files_list.append(config_files_dict['user'])
        else:
            try:
                constants.config_user.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError as e:
                msg=f'could not create user configuration directory: {constants.config_user.parent}'
                logging.critical(msg)
                do_exit(1, msg)
            try:
                shutil.copy(constants.config_base, constants.config_user)
            except Exception as e:
                msg=f'could not copy user configuration file to {constants.config_user}'
                logging.critical(1, msg)
                do_exit(1, msg)
            msg = f'''This appears to be the first time PaperPi has been run.
A user configuration file created: {constants.config_user}
At minimum you edit this file and add a display_type and enable one plugin.
        
Edit the configuration file with:
   $ nano {constants.config_user}'''
            do_exit(0, msg)
            
    
    
            
    logging.info(f'using configuration files to configure PaperPi: {config_files_list}')
    config_files = ArgConfigParse.ConfigFile(config_files_list, ignore_missing=True)
    try:
        config_files.parse_config()
    except DuplicateSectionError as e:
        logging.error(f'{e}')
        config_files = None

    return config_files
        
        






def sanitize_vals(config):
    '''attempt to convert all the strings in config into appropriate formats
             float like strings ('7.1', '100.2', '-1.3') -> to float
             int like strings ('1', '100', -12) -> int
             boolean like strings (yes, no, Y, t, f, on, off) -> 0 or 1
         Args:
             config(`dict`): nested config.ini style dictionary

         Returns:
             `dict`'''    
    def strtofloat(s):
        '''convert strings to float if possible on failure return original value
        
        Args:
            s(any type): if s is of type string attempt to conver to float'''
        retval = s
        if isinstance(s, str):
            if '.' in s:
                try:
                    retval = float(s)
                except ValueError:
                    pass

        return retval

    def convert(d, new_type, exceptions):
        '''convert value to new_type handling exceptions appropriately
        
        d(any type): if d is of type str attempt to convert to new_type
        new_type(Type): type to convert d into
        exceptions(tuple of Exceptions): tuple of exception types to expect'''
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
    
    # first try to convert strings to float
    convert(config, strtofloat, ValueError)
    # convert remaining strings to int
    convert(config, int, (ValueError))
    # convert remaining strings into booleans (if possible)
    # use the distuitls strtobool function
    convert(config, strtobool, (ValueError, AttributeError))
    
    # return converted values and original strings
    
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
        splash = Plugin(**splash_config)
        splash.update(constants.app_name, constants.version, constants.url)

        logging.debug(f'splash screen image type: {type(splash.image)}')
    return splash






def setup_display(config):
    def ret_obj(obj=None, status=0, message=None):
        return{'obj': obj, 'status': status, 'message': message}    
    keyError_fmt = 'configuration KeyError: section[{}], key: {}'

    moduleNotFoundError_fmt = 'could not load epd module: {} -- error: {}'
    
    epd = config['main']['display_type']
    vcom = config['main']['vcom']
    try:
        screen = Screen(epd=epd, vcom=vcom)
        screen.clearEPD()
    except ScreenError as e:
        logging.critical('Error loading epd from configuration')
        return_val = ret_obj(None, 1, moduleNotFoundError_fmt.format(epd, e))
        return return_val
    except PermissionError as e:
        logging.critical(f'Error initializing EPD: {e}')
        logging.critical(f'The user executing {constants.app_name} does not have access to the SPI device.')
        return_val = ret_obj(None, 1, 'This user does not have access to the SPI group\nThis can typically be resolved by running:\n$ sudo groupadd <username> spi')
        return return_val
    except FileNotFoundError as e:
        logging.critical(f'Error initializing EPD: {e}')
        logging.critical(f'It appears that SPI is not enabled on this Pi. See: https://github.com/txoof/epd_display/tree/testing#hardwareos-setup')
        return_val = ret_obj(None, 1, moduleNotFoundError_fmt.format(epd, e))
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
    '''Build a dictionary of configured plugin objects
    
    Args:
        config(dict): configuration dictionary 
        resolution(tuple): X, Y resolution of screen
        cache(obj: Cache): cache object for managing downloads of images
        
    Returns:
        dict of Plugin'''
    # get the expected key-word args from the Plugin() spec
    spec_kwargs = getfullargspec(Plugin).args

    plugins = []

   # configure fall-back plugin with extremely low priority to display if all else fails
    my_config = {}
    logging.info('adding default plugin to plugin loop')
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
            # force layout to one-bit mode for non-HD screens
            my_config['force_onebit'] = config['main']['force_onebit']
            
            try:
                module = import_module(f'{constants.plugins}.{values["plugin"]}')
                my_config['update_function'] = module.update_function
                my_config['layout'] = getattr(module.layout, values['layout'])
            except KeyError as e:
                logging.info('no module specified; skipping update_function and layout')
                continue
            except ModuleNotFoundError as e:
                logging.warning(f'error: {e} while loading module {constants.plugins}.{values["plugin"]}')
                logging.warning(f'skipping plugin')
                continue
            except AttributeError as e:
                logging.warning(f'could not find layout "{my_config["layout"]}" in {my_config["name"]}')
                logging.warning(f'skipping plugin')
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
        
    return plugins






def update_loop(plugins, screen, max_refresh=5):
    def update_plugins(force_update=False):
        logging.info(f'[[..........UPDATING PLUGINS..........]]')
        logging.debug(f'{len(plugins)} plugins in list')
        my_priority_list = [2**15]
        for plugin in plugins:
            logging.info(f"{'_'*10}{plugin.name}{'_'*10}")
            if force_update:
                logging.info('FORCING UPDATE')
                plugin.force_update()
            else:
                plugin.update()
                
            logging.info(f'PRIORTITY: {plugin.priority} of {plugin.max_priority}')
            my_priority_list.append(plugin.priority)
            
            logging.debug(f'DATA: {plugin.data}')
            logging.debug(f'IMAGE: {plugin.image}')
            logging.debug(f'IMAGE STRING: {str(plugin.image)}')

        return my_priority_list
    
    logging.debug(f'max_refresh = {max_refresh}')
    
    logging.info('starting update loop')
    exit_code = 1
    priority_list = []
    priority_list = update_plugins(force_update=True)
    plugin_cycle = cycle(plugins)
    current_plugin = next(plugin_cycle)
    refresh_count = 0
    current_hash = ''

    
    # lower numbers are of greater importance
    max_priority = min(priority_list)
    
    last_priority = max_priority
    
    
    for i in range(0, len(plugins)):
        if current_plugin.priority <= max_priority:
            current_timer = Update()
            current_plugin_active = True
            logging.info(f'FIRST DISPLAY PLUGIN: {current_plugin.name}')
            break
        else:
            current_plugin = next(plugin_cycle)
    
#     with InterruptHandler() as h:
    interrupt_handler = InterruptHandler()
    while not interrupt_handler.kill_now:
#         if h.interrupted:
#             logging.info('caught interrupt, stopping execution')
#             exit_code = 0
#             break
        logging.info(f'{current_plugin.name} time remaining: {current_plugin.min_display_time-current_timer.last_updated:.1f} of {current_plugin.min_display_time}')

        priority_list = update_plugins()
        last_priority = max_priority
        max_priority = min(priority_list)


        # if the timer has expired or the priority has increased, display a different plugin
        if current_timer.last_updated > current_plugin.min_display_time:
            logging.info(f'display_time elapsed, cycling to next active plugin')
            current_plugin_active = False

        if max_priority > last_priority:
            logging.info(f'priority level has increased, cycling to higher priority plugin')
            current_plugin_active = False

        # cycle no more than once through plugins looking for next active plugin
        if not current_plugin_active:
            logging.debug('searching for next active plugin')
            for attempt in range(0, len(plugins)):
                current_plugin = next(plugin_cycle)
                logging.debug(f'checking plugin: {current_plugin.name}')
                if current_plugin.priority <= max_priority:
                    current_plugin_active = True
                    logging.debug(f'using pluign: {current_plugin.name}')
                    current_timer.update()
                    break

        # check the unique data-hash for each plugin & only write when data has updated
        if current_hash != current_plugin.hash:
            logging.debug('screen refresh required')
            current_hash = current_plugin.hash

            # do total wipe of HD Screens after max_refresh writes
            if refresh_count >= max_refresh-1 and screen.HD:
                logging.debug(f'{refresh_count} reached of maximum {max_refresh}')
                refresh_count = 0
                screen.clearEPD()

            try:
                screen.writeEPD(current_plugin.image)
                refresh_count += 1
            except FileNotFoundError as e:
                msg = 'SPI does not appear to be enabled. Paperpi requires SPI access'
                logging.critical(msg)
                do_exit(1, msg)
            except ScreenError as e:
                logging.critical(f'{current_plugin.name} returned invalid image data; screen update skipped')
                logging.debug(f'DATA: {current_plugin.data}')
                logging.debug(f'IMAGE: {current_plugin.image}')
                logging.debug(f'IMAGE STRING: {str(current_plugin.image)}')
                current_plugin_active = False
        else:
            logging.debug('plugin data not refreshed, skipping screen update')


        sleep(2)
    # report the exit of main display loop
    logging.info(f'Interrupt signal recieved: {interrupt_handler.kill_signal_name}')
    exit_code = 0

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
    if not config_files:
        print('Fatal Error collecting config files! See the logs!')
        return
    
    # merge file and commandline (right-most over-writes left)
    config = ArgConfigParse.merge_dict(config_files.config_dict, cmd_args.nested_opts_dict)
    
    if cmd_args.options.version:
        print(constants.version_string)
        return
    
    if cmd_args.options.plugin_info:
        get_help.get_help(cmd_args.options.plugin_info)
        return
    
    if cmd_args.options.list_plugins:
        get_help.get_help()
        return
    
    if cmd_args.options.run_plugin_func:
        run_module.run_module(cmd_args.options.run_plugin_func)
        return
    
    if cmd_args.options.add_config:
        try:
            my_plugin = cmd_args.options.add_config[0]
            config_opt = cmd_args.options.add_config[1]
        except IndexError:
            my_plugin = None
            config_opt = None
            
        if config_opt == 'user':
            config_opt = constants.config_user
        elif config_opt == 'daemon':
            config_opt = constants.config_system
        else:
            config_opt = None
        
        run_module.add_config(module=my_plugin, config_file=config_opt)
        return
    
    # make sure all the integer-like strings are converted into integers
    config = sanitize_vals(config)
#     return config
    
    
    logger.setLevel(config['main']['log_level'])
    logging.root.setLevel(config['main']['log_level'])
    
    logging.info(f'********** PaperPi {constants.version} Starting **********')
    
    logging.debug(f'configuration:\n{config}')
    
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
        splash.force_update(constants.app_name, constants.version, constants.url)
        logging.debug('displaying splash screen')
        logging.debug(f'image type: {type(splash.image)}')
        try:
            screen.writeEPD(splash.image)
        except FileNotFoundError as e:
            msg = 'SPI does not appear to be enabled. Paperpi requires SPI access'
            logging.critical(msg)
            do_exit(1, msg)            
        except ScreenError as e:
            logging.critical(f'Could not write to EPD: {e}')
    
    
    cache = CacheFiles(path_prefix=constants.app_name)
    
    # force one bit mode if screen is NOT HD
    if screen.HD:
        config['main']['force_onebit'] = False
    else:
        config['main']['force_onebit'] = True

    plugins = build_plugin_list(config=config, resolution=screen.resolution, cache=cache)

#     return plugins, screen, cache
    
    exit_code = update_loop(plugins=plugins, screen=screen, max_refresh=config['main']['max_refresh'])

    logging.info('caught terminate signal -- cleaning up and exiting')
    clean_up(cache, screen)
    
    return exit_code






# s = [i for i in sys.argv]






# sys.argv = [i for i in s]
# sys.argv






# sys.argv.extend(['--add_config', 'reddit_quote', 'daemon'])






if __name__ == "__main__":
    # remove jupyter runtime junk for testing
    if len(sys.argv) >= 2 and 'ipykernel' in sys.argv[0]:
        t = 'foo'
        r = sys.argv[3:]
        sys.argv = [t]
        sys.argv.extend(r)
#         sys.argv = [sys.argv[0]]
#         sys.argv.extend(sys.argv[2:])
    exit_code = main()
    sys.exit(exit_code)








# logger = logging.getLogger(__name__)
# logger.root.setLevel('DEBUG')


