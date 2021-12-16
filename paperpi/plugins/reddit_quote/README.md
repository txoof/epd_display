# reddit_quote
![sample image for plugin reddit_quote](./reddit_quote_sample.png)
```
 
PLUGIN: reddit_quote v:0.1.0

 
FUNCTION: update_function
update function for reddit_quote plugin
    
    Scrapes quotes from reddit.com/r/quotes and displays them one at a time
    
   Requirements:
        self.config(`dict`): {
        'max_length': 144,   # name of player to track
        'idle_timeout': 10,               # timeout for disabling plugin
    }
    self.cache(`CacheFiles` object)

    Args:
        self(namespace): namespace from plugin object
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))        
    
    
___________________________________________________________________________
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.reddit_quote.reddit_quote

# this is a sample config users can use to help setup the plugin
[Plugin: Reddit Quotes]
# default layout
layout = layout
# the literal name of your module
plugin = reddit_quote
# recommended display time
min_display_time = 50
# maximum priority in display loop
max_priority = 2
# maximum length of quote (in characters including spaces, a la Twitter
max_length = 144

 
LAYOUTS AVAILABLE:
  layout
  quote
  quote_inverse
  quote_small_screen
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.reddit_quote.reddit_quote:
```

## Additional Plugin Information
