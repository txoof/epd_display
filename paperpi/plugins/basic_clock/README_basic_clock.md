# basic_clock
![sample image for plugin basic_clock](basic_clock_sample.png)
```

PLUGIN: basic_clock v:0.1.0


FUNCTION: update_function
provides system time string in the format HH:MM
    
    Args:
        None
    
    Returns:
        dict: {'digit_time': HH:MM string}
    
___________________________________________________________________________
 


SAMPLE CONFIGURATION FOR plugins.basic_clock.basic_clock

[Plugin: Basic Clock]
layout = layout
plugin = basic_clock
refresh_rate = 55
min_display_time = 60
max_priority = 2


LAYOUTS AVAILABLE:
  basic_clock
  layout


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.basic_clock.basic_clock:
   digit_time
```