# stringmaker.py
# David Prager Branner
# 20140329

import string
import random

class StringMaker():
    def __init__(self):
        self.germ_w_space=False
        self.germ_w_tab=False
        self.germ_w_CR=False
        self.fill_w_space=False
        self.fill_w_tab=False
        self.fill_w_CR=False

    def string_w_repeats():
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
