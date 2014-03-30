# stringmaker.py
# David Prager Branner
# 20140329

import string
import random

def stringmaker():
    repeats = random.randint(1, 5)
    string_length = random.randint(1, 10)
    germ = ''join([random.choice(string.ascii_lowercase, 1) 
            for i in range string_length])
