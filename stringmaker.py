# stringmaker.py
# David Prager Branner
# 20140329

"""Construct various "attack" strings for Regex Blaster."""

import string
import random

class StringMaker():
    def __init__(self):
        self.germ_w_space=False
        self.germ_w_tab=False
        self.germ_w_LF=False
        self.germ_kinds = {
                self.germ_w_space: ' ',
                self.germ_w_tab: '\t',
                self.germ_w_LF: '\n'}
        self.fill_w_space=False
        self.fill_w_tab=False
        self.fill_w_LF=False
        self.fill_kinds = {
                self.fill_w_space: ' ',
                self.fill_w_tab: '\t',
                self.fill_w_LF: '\n'}

    def add_cruft(self, base):
        for kind in kinds:
            if kind:
                base += self.kinds[kind] * len(base) / 2

    def make_string(self):
        germ_stuff = string.ascii_lowercase
        if self.germ_w_space:
            germ_stuff += ' ' * 13
        if self.germ_w_tab:
            germ_stuff += '\t' * 13
        if self.germ_w_LF:
            germ_stuff += '\n' * 13
        fill_stuff = string.ascii_uppercase
        if self.fill_w_space:
            fill_stuff += ' '
        if self.fill_w_tab:
            fill_stuff += '\t'
        if self.fill_w_LF:
            fill_stuff += '\n'
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
