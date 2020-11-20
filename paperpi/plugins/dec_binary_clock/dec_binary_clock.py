#!/usr/bin/env python3
# coding: utf-8




from datetime import datetime
from PIL import Image, ImageDraw
import re
import logging






try:
    from . import layout
    from . import constants
except ImportError:
    import layout 
    import constants






logger = logging.getLogger(__name__)






def split_place_value(d):
    tens = int((d-(d%10))/10)
    ones = int(d-tens*10)
    return tens, ones






def time_now():
    return datetime.now().strftime("%H:%M")






def split_by_place(d):
    num_list = [i for i in str(d)]
    return num_list






def dec2bin(d, min_bits=4):
    bin_array = []
    whole = d
    while whole > 0:
        remainder = whole%2
        whole = int(whole/2)
        bin_array.append(remainder)
    if len(bin_array) < min_bits:
        for i in range(min_bits-len(bin_array)):
            bin_array.append(0)
    
    return bin_array[::-1]






def dot_array(r, border, array, padding):
    dim = [(r*2)+padding*2, len(array)*(r*2)+padding*(len(array)+1)] 
    image = Image.new('1', dim, color=1)
    d = ImageDraw.Draw(image)
    for idx, val in enumerate(array):
        topOuter = [0+padding, (r*2*idx)+padding+padding*idx]
        bottomOuter = [r*2+padding, r*2*(idx+1)+padding+padding*idx]
        topInner = [topOuter[0]+border, topOuter[1]+border]
        bottomInner = [bottomOuter[0]-border, bottomOuter[1]-border]
        d.ellipse(topOuter+bottomOuter, fill=0)
        if val==0:
            d.ellipse(topInner+bottomInner, fill=1)
    
    return image






def separator(dim, padding, fill=60):
    dim = [dim[0]+padding, dim[1]+padding]
    top = [padding, padding]
    bottom = dim
    i = Image.new('1', (dim[0], int(dim[1]*fill/60)), color=1)
    d = ImageDraw.Draw(i)
    d.rectangle(top+bottom, fill=0)
    
    return i






def update_function(self=None, time=None):
    '''update function for dec_binary_clock 
    
    This plugin provides time as an image and string in 
    four, four-bit numbers in little-endian format (see EXAMPLE).
    
    
    
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
        
    Returns:
        tuple: (is_updated(bool), data(dict), priority(int))
        
    %U'''
    r = 80
    border = 10
    padding = 10
    time_array = []
    img_x = 0
    img_y = 0
    img_array = []
    return_time = None

    logging.debug(f'TIME = {time}')
    
    # break the time string into digits if provided
    if time:
        return_time = str(time)
        time = str(time)
        match = re.search('([0-9]{1,2}):([0-9]{1,2})', time)
        hour = match.group(1)
        minute = match.group(2)
    else:
        hour = datetime.now().hour
        minute = datetime.now().minute
        return_time = f'{hour:02}:{minute:02}'
    
    
    # make sure there are two digits in hour
    if len(str(hour)) < 2:
        time_array = [0]
    
    # join up the hours and the colon 
    time_array = time_array + split_by_place(hour) + [-1]
    
    # make sure there are two digits in minute
    if len(str(minute)) < 2:
        time_array = time_array + [0]
    
    # join up the hours, colon and minute
    time_array = time_array + split_by_place(minute)
        
    # build an array of the images
    for i in time_array:
        i = int(i)
        # separator is represented by a negative number
        if i < 0:
            img_array.append(separator(dim=[int(r/2), 4*(r*2)+padding*5], padding=0))
        # create a dot array for each decimal place
        else:
            img_array.append(dot_array(r=r, border=border, padding=padding, array=dec2bin(i)))
    
    # determine dimensions of array
    for j in img_array:
        img_x = img_x + j.width
        if j.height > img_y:
            img_y = j.height
            
    # create a blank image
    img = Image.new('1', [img_x, img_y], color=1)
    
    # build the composite image
    x_pos = 0
    y_pos = 0
    for j in img_array:
        img.paste(j, [x_pos, y_pos])
        x_pos = x_pos + j.width
    
    return (True, {'bin_img': img, 'time': return_time}, self.max_priority)











