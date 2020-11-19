# word_clock
![sample image for plugin word_clock](documentation/images/word_clock_sample.png)
```

PLUGIN: word_clock v:0.1.0


FUNCTION: update_function
update function for word_time plugin
    provides aproximate time in words
    
    Example:
        The time is around ten twenty
        It is about twenty after eight
    
    Args:
        self(`namespace`)
        time(`str`): time as a string in format HH:MM (primarily used for testing)
    
___________________________________________________________________________
 


SAMPLE CONFIGURATION FOR plugins.word_clock.word_clock

[Plugin: Word Clock]
layout = layout
plugin = word_clock
refresh_rate = 100
min_display_time = 30
max_priority = 2


LAYOUTS AVAILABLE:
  layout
  word_clock
  word_clock_lg


DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY plugins.word_clock.word_clock:
   word_time
   time
```