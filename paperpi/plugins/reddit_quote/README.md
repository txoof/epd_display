# reddit_quote
![sample image for plugin paperpi.plugins.reddit_quote](./reddit_quote.layout-sample.png) 

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

[Plugin: Reddit Quotes]
layout = layout
plugin = reddit_quote
refresh_rate = 100
min_display_time = 50
max_priority = 2
# maximum length of quote (in characters) including spaces, a la Twitter
max_length = 144

 
LAYOUTS AVAILABLE:
  layout
  quote
  quote_inverse
  quote_small_screen
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.reddit_quote.reddit_quote:
```

## Provided Layouts:

layout: **layout**

![sample image for plugin layout](./reddit_quote.layout-sample.png) 


layout: **quote**

![sample image for plugin quote](./reddit_quote.quote-sample.png) 


layout: **quote_inverse**

![sample image for plugin quote_inverse](./reddit_quote.quote_inverse-sample.png) 


layout: **quote_small_screen**

![sample image for plugin quote_small_screen](./reddit_quote.quote_small_screen-sample.png) 


## Additional Plugin Information
This plugin is based on the [veebch/stonks](https://github.com/veebch/stonks) application. The code is mostly rewritten, but the basic layout and much of the logic is borrowed.