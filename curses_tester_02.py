#! /usr/bin/python
# curses_tester_02.py
# David Prager Branner
# 20140401

"""Explore the use of Ncurses.

02 Set up and close curses in special functions; always trap ctrl-c.
01 Open window; close on two backticks.
"""

import sys
if sys.version_info[0] != 3:
    print('Python 3 required.')
    sys.exit()
import curses

def main():
    stdscr = set_up_curses()
    ctrl_c_loop()
    close_curses(stdscr)


###################
# Body of program #
###################

def main_loop():
    window = curses.newwin(curses.LINES, curses.COLS)
    c = window.getch()
    if c == ord('`'):
        c = window.getch()
        if c == ord('`'):
            return True

# Things to do:
# Different subwindows.
# Find current window dimensions.
# Set background color.
# Item gradually fading into view.
# Input box.

#######################
# End of program body #
#######################

#######################
# Curses housekeeping #
#######################

def set_up_curses():
    # Instantiate standard screen object.
    stdscr = curses.initscr()
    # Properly initialize screen.
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    # Check for and begin color support.
    if curses.has_colors():
        curses.start_color()
    # Optionally enable the F-1 etc. keys, which are multi-byte.
    stdscr.keypad(1)
    return stdscr

def ctrl_c_loop():
    while True:
        try:
            if main_loop():
                break
        except KeyboardInterrupt:
            continue

def close_curses(stdscr):
    # If program core finished, restore terminal settings.
    curses.nocbreak() # end character-break mode.
    stdscr.keypad(0)
    curses.echo()
    curses.curs_set(1)

    # Destroy window.
    curses.endwin()

if __name__ == '__main__':
    main()
