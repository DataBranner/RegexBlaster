# curses_tester.py
# David Prager Branner
# 20140401

"""Explore the use of Ncurses."""

import curses
from urllib2 import urlopen
from HTMLParser import HTMLParser
from simplejson import loads

nstantiate standard screen object
stdscr = curses.initscr()

# Properly initialize screen
curses.noecho()
curses.cbreak()
curses.curs_set(0)

# check for and begin color support
if curses.has_colors():
    curses.start_color()

# optionally enable the F-1 etc. keys, which are multi-byte
strdscr.keypad(1)

###################
# Body of program #
###################

# Things to do:
# Different subwindows.
# Find current window dimensions.
# Set background color.
# Item gradually fading into view.
# Input box.

###################
# End of program  #
###################


# if broken out of loop, restore terminal settings
curses.nocbreak() # end character-break mode
stdscr.keypad(0)
curses.echo()
curses.curs_set(1)

# destroy window
curses.endwin()



