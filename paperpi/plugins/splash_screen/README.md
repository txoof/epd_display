# splash_screen
![sample image for plugin paperpi.plugins.splash_screen](./splash_screen.layout-sample.png) 

```
 
PLUGIN: splash_screen v:0.1.0

 
FUNCTION: update_function
update function for splash_screen provides program name, version, url
    
    This plugin provides a basic splash screen with application 
    name, version and url
    
    Requirements:
        None
        
    Args:
        self(`namespace`)
        app_name(`str`): application name
        version(`str`): version number
        url(`str`) url
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))        
    
___________________________________________________________________________
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.splash_screen.splash_screen
no sample configuration provided in paperpi.plugins.splash_screen.splash_screen.constants
 
LAYOUTS AVAILABLE:
  layout
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.splash_screen.splash_screen:
   app_name
   version
   url
```

## Provided Layouts:

layout: **layout**

![sample image for plugin layout](./splash_screen.layout-sample.png) 


