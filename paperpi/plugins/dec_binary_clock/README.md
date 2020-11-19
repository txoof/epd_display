# mod_name
![sample image for plugin <module 'plugins.dec_binary_clock' from '/home/pi/src/epd_display/paperpi/plugins/dec_binary_clock/__init__.py'>](../documentation/images/dec_binary_clock_sample.png)
```

FUNCTION: update_function
update function for dec_binary_clock 
    provides time as an image in four, four-bit numbers in little-endian format:
    
    EXAMPLE:
    Time 14:49
    o o | o x
    o x | x o
    o o | o o
    x o | o x 
    
    Requirements:
        None
        
    Args:
        self(`object namespace`)
        time(`str`): HH:MM formatted string to display (this is primarily for testing)
    
___________________________________________________________________________
 
```