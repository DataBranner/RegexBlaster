# stringmaker.py
# David Prager Branner
# 20140329

import string
import random

def string_w_repeats(w_space=False, w_tab=False, w_CR=False):
    germ_stuff = string.ascii_lowercase
    fill_stuff = string.ascii_uppercase
    repeats = random.randint(2, 5)
    string_length = random.randint(2, 5)
    germ = ''.join([random.choice(germ_stuff) for i in range(string_length)])
    string_length = random.randint(1, string_length+1)
    string_w_repeats = ''
    for i in range(repeats):
        string_w_repeats += (germ + ''.join([random.choice(fill_stuff)
            for i in range(string_length)]))
    return string_w_repeats

def string_w_spaces():
    pass
