version = '0.1.1'

name = 'word_time'

data = {
        'word_time': 'string containing time',
        'time': 'string containing time as HH:MM',
       }

hours = {'1':  ['one', 'late'],
         '2':  ['two', 'really late', 'go to bed'],
         '3':  ['three', 'too late', "why aren't you in bed"],
         '4':  ['four', 'early morning', 'stupid early'],
         '5':  ['five', 'crack of dark'],
         '6':  ['six', 'crack of dawn'],
         '7':  ['seven'],
         '8':  ['eight'],
         '9':  ['nine'],
         '10': ['ten'],
         '11': ['eleven'],
         '12': ['noon', 'twelve', 'lunch'],
         '13': ['one'],
         '14': ['two'],
         '15': ['three'],
         '16': ['four'],
         '17': ['five'],
         '18': ['six'],
         '19': ['seven'],
         '20': ['eight'],
         '21': ['nine'],
         '22': ['ten'],
         '23': ['eleven'],
         '0' : ['midnight', 'twelve', 'dark']}

minutes = {'0': ["'o clock", "on the dot"],
           '6': ["'o clock", "on the dot"],
           '1': ['ten after'],
           '2': ['twenty after'],
           '3': ['half past', 'thirty after', 'thirty past', ],
           '4': ["twenty 'til"],
           '5': ["ten 'til"]}

stems = ['The time is nearly', 
         "It is about", 
         "It is around", 
         "It is almost",
         "It is close to",
         "It's round about",
         "It's nearly",
        ]

sample_config = '''
[Plugin: Word Clock]
layout = layout
plugin = word_clock
refresh_rate = 125
min_display_time = 255
max_priority = 2
'''
