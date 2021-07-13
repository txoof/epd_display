# newyorker
![sample image for plugin newyorker](./newyorker_sample.png)
```
 
PLUGIN: newyorker v:0.0.1

 
FUNCTION: update_function
update function for newyorker provides a New Yorker comic of the day
    
    This plugin provides an image and text pulled from the New Yorker 
    
    Requirments:
        self.config(dict): {
            'day_range': 'number of days to pull comics from (default: 5)',
        }    
    
    Args:
        self(`namespace`)
        day_range(`int`): number of days in the past to pull radom comic and text from
            use 1 to only pull from today
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))    
    
___________________________________________________________________________
 
 

SAMPLE CONFIGURATION FOR paperpi.plugins.newyorker.newyorker
no sample configuration provided in paperpi.plugins.newyorker.newyorker.constants
 
LAYOUTS AVAILABLE:
  default
  layout
 

DATA KEYS AVAILABLE FOR USE IN LAYOUTS PROVIDED BY paperpi.plugins.newyorker.newyorker:
   comic
   text
   time
```

