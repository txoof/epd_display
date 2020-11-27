# demo_plugin
![sample image for plugin demo_plugin](./demo_plugin_sample.png)
```
 
PLUGIN: demo_plugin v:0.1.0

 
FUNCTION: demo_function
demo function that prints a docstring
    
    This function prints the __doc__ string for this function as a 
    demonstration of a Plugin "user-facing" function.
    
    Args:
        None
        
    Returns:
        None
    
___________________________________________________________________________
 
FUNCTION: update_function
update function for demo plugin providing some silly information and a picture
    
    This plugin provides a message generated for the user and 
    a static image that floats around
    
    Requirments:
        self.config(dict): {
            'your_name': 'user name',
            'your_color': 'user color',
        }
        
    Args: 
        self(namespace): namespace from plugin object
    
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))

    # Don't forget to end your docstring with a "" so it is displayed
    
___________________________________________________________________________
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.demo_plugin.demo_plugin
`
# this is a sample config users can use to help setup the plugin
[Plugin: A Demo Plugin]
# default layout
layout = layout
# the literal name of your module
plugin = demo_plugin
# recommended display time
min_display_time = 30
# maximum priority in display loop
max_priority = 1
# your name
your_name = Slartybartfast
# your favorite color
your_color = chartreuse

 
LAYOUTS AVAILABLE:
  layout
  my_layout_one
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.demo_plugin.demo_plugin:
   welcome_str
   time
   extra
   image
```

## Additional Plugin Information
Additional plugin information can be appended to the README by adding a file called `README_additional.md` in the root of the plugin directory. This will be directly appened at the end of the README.md file.


Included image was sourced from the [Wikimedia Project](https://commons.wikimedia.org/wiki/File:Acuminate_Leaf_\(PSF\).jpg)
