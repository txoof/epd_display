#!/usr/bin/env python3
# coding: utf-8




import logging
from datetime import datetime
from random import choice






try:
    from . import layout
    from . import constants
except ImportError:
    import layout 
    import constants






def time_list(time):
    '''Returns time as list [h, m] of type int
    
    Args:
        time(`str`): time in colon separated format - 09:34; 23:15'''
    return  [int(i)  for i in time.split(':')]






def time_now():
    return datetime.now().strftime("%H:%M")






def map_val(a, b, s):
    '''map range `a` to `b` for value `s`

    Args:
        a(2 `tuple` of `int`): (start, end) of input values
        b(2 `tuple` of `int`): (start, end) of output values
        s(`float`, `int`): value to map
    Returns:
        `int`'''
    a1, a2 = a
    b1, b2 = b
    
    t = b1 + ((s-a1) * (b2-b1))/(a2-a1)
    
    return round(t)






def update_function(self, time=None):
    '''update function for word_clock provides time as text
    
    This plugin provides the time as a string such as:
        * The time is around ten twenty
        * It is about twenty after eight
    
    Args:
        self(`namespace`)
        time(`str`): time as a string in format HH:MM (primarily used for testing)
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))    
    %U'''
    logging.info(f'update_function for {self.name}')
    hours = constants.hours
    minutes = constants.minutes
    stems = constants.stems
    
    if time:
        now = time
        logging.debug(f'using {time}')
        t_list = time_list(time)
    else:
        now = time_now()
        logging.debug(f'using {now}')
        t_list = time_list(now)
        
    # this range shifts the period of the list so times around the 'tens' round nicely up and down        
    minute = map_val((1, 59), (0, 6), t_list[1])

    # set the hour appropriately - from 'after' to 'til'
    if t_list[1] <= 34:
        hour_str = hours[str(t_list[0])]
    else:
        try:
            hour_str = hours[str(t_list[0]+1)]
        except KeyError as e:
            # wrap around to zero'th index in the hours list
            hour_str = hours[str(t_list[0]+1 - len(hours))]
            hour_str = hours[str(0)]
        
    min_str = minutes[str(minute)]
    
    # properly organize the time string
    # 'o clock times
    if minute == 0 or minute == 6:
        time_str = f'{choice(hour_str).title()} {choice(min_str).title()}'
                      
    else: 
        time_str = f'{choice(min_str).title()} {choice(hour_str).title()}'
    
    
    myTime = {'wordtime': f'{choice(stems)} {time_str}',
              'time': now}
    
    return (True, myTime, self.max_priority)











