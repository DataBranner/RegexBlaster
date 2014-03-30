# stringmaker.py
# David Prager Branner
# 20140329

import string
import random

def string_w_repeats():
    repeats = random.randint(2, 5)
    string_length = random.randint(2, 5)
    germ = ''.join([random.choice(string.ascii_lowercase)
            for i in range(string_length)])
    string_length = random.randint(1, string_length+1)
    string_w_repeats = ''
    for i in range(repeats):
        string_w_repeats += (germ + 
                ''.join([random.choice(string.ascii_uppercase)
                    for i in range(string_length)]))
    return string_w_repeats

