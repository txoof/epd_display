# Plugins
All plugins are configured through the `paperpi.ini` files. For a single-user configuration the file is stored in `~/.config/com.txoof.paperpi/` for system-wide daemon configuration the file is stored in `/etc/defaults/`.


## Configuration
Each plugin must have the following configuration at a minimum:

*NB!: whitespace and comments are ignored*
```
[Plugin: Human Friendly Name For Plugin]
layout = layout
plugin = plugin_name
refresh_rate = int
max_priority = int
```

### Configuration Elements
**Section Header**: `[Plugin: Human-Friendly Name for Plugin]`
* all plugin sections must **start** with `[Plugin: XXXX]` where XXX is a user-chosen descriptive string
* enabled: `[Plugin: name]`
* disabled: `[xPlugin: name]`

**Plugin Name**: `plugin = plugin_name`
* module name of plugin
* use `--list_plugins` to see available plugin names

**Layout Definition**: `layout = layout`
* screen layout that defines how to organize plugin graphical and text elements
* use `--plugin_info plugin_name` to see available layouts

**Refresh Rate**: `refresh_rate = integer in seconds`
* this controls how often the plugin is checked for new data
* some services such as spotify or MET.NO will ban users that request updates too frequently. Use caution when setting this.
* each plugin has a recommended `refresh_rate` use `--plugin_info plugin_name` to view a sample configuration

**max_priority**: `max_priority = integer`
* **LOWER** numbers are a higher priority (-1 is very high and will likely display immediately, 64000 will never be shown)
* a music plugin should likely be set to `0` to ensure that when a track change happens the display is updated
* a clock plugin that displays when music players are idle should be set to 2
* plugins with the lowest integer value will be displayed in the display loop
* some plugins change their priority when events happen such as when an audio track changes, music is paused, or a device becomes idle
* this value determines the maximum priority the plugin will use when it determines an important event has occured.
* recommended values can be found by using `--plugin_info plugin_name`


### Additional Configuration Elements
Some plugins require additonal configuration such as API keys, location information or other configuration details. Use `--plugin_info plugin_name` to find a sample configuration. Check the plugin README for additional information.

## Writing Plugins
PaperPi is designed to support additional plugins. See the included `demo_plugin` for a simple, well documented plugin that can be used as a template for building a plugin.

Plugins are written in python 3 and should follow the following guidelines to function properly:
* Plugin modules must be added to the `plugins` directory
* Plugin modules must be named with exactly the same name as their module directory:
    - `plugins/my_new_plugin/my_new_plugin.py
* Include a `__init__.py` file that contains:
    - `from .my_new_plugin import update_function`
* Plugin modules must contain at minimum one function called `update_function()`
    - see below for a complete spec for the `update_function`
* Plugin modules will receive any configuration options specified in it's configuration section in the  `paperpi.ini` file at startup
    - Any values your plugin requires such as API keys, email addresses, URLs can be accessed from the `self.config` property 
* Plugin modules must at minimum contain a `layout.py` file that contains a layout file. 
    - The default layout should be named `layout`
        - it is acceptable to set `layout = my_complex_name` for the default playout
    - See the [epdlib Layout module](https://github.com/txoof/epdlib#layout-module)
    - See the `basic_clock` plugin for a simple layout template
* Plugin modules may have user-facing helper functions that can help the user setup or configure the plugin
    - See the `lms_client` plugin and the `met_no` plugins for examples
* At minimum the `update_function` should contain a docstring that completely documents the plugin's use and behavior
    - See the example below
    - End all user-facing docstrings with `%U`; to ensure they are included in the auto-documenting build scripts
* Plugin modules should contain a `constants.py` file that contains:
    - `version='version string'
    - `name='name of plugin'`
    - `data = {
            'key1': 'description of value',
            'key2': 'description of value',
            'keyN': 'description of value',
    }
    - `sample_config = '''
    [Plugin: My New Plugin]
    layout = layout
    plugin = my_new_plugin
    config_opt1 = some_value
    config_optN = 123456
    max_display_time = 45
    max_priority = 1
    '''
* Plugin modules should contain a `sample.py` file that contains sample data for creating documentation
    - See the specificaiton below
    
**`update_function` specifications**
The update_function is added to a `library.Plugin()` object as a method. The update_function will have access to the `self` namespace of the Plugin object including the `max_priority` and `cache`. The `Plugin()` API is well documented.

* `update_function` must accept `*args, **kwargs` even if they are not used
* `update_function` must return a tuple of: (is_updated(bool), data(dict), priority(int))
    - `is_updated` indicates if the module is up-to-date and functioning; return `False` if your module is not functioning properly or is not opperating
    - `data` is a dictionary that contains key/value pairs of either strings or an image (path to an image or PIL image object).
    - `priority` indicates your modules priority
        - The default should be to return `self.max_priority`; it is allowed to return `self.max_priority - 1` if your plugin detects an important event.
        - If the module is in a passive state (e.g. there is no interesting data to show) set `priority` to `2**15` to ensure it is not included in the display loop
* Example docstring:
    ```
    '''
    update function for my_plugin_name provides foo information
    
    This plugin provides...
    
    Requirements:
        self.config(dict): {
            key1: value1
            key2: value2
        }
        self.cache(CacheFiles object): location to store downloaded images
        
    Args:
       self(namespace): namespace from plugin object
     
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))
    %U'''
    ```

**`sample.py` specifications**
To provide a sample image and automatically create documentation provide a `sample.py` file with your module with the following information:
`config = {
    # this is required
    'layout': 'layout_name_to_use_for_sample_img',
    # optional below this point
    'config_option': 'value',
    'config_option2': 12345
}

## Plugins Currently Avialable
