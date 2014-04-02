#! /usr/bin/python
# curses_tester_03.py
# David Prager Branner
# 20140401

"""Explore the use of Ncurses.

next: Set up different sub-windows.
03 Get styled text working.
02 Set up and close curses in special functions; always trap ctrl-c.
01 Open window; close on two backticks.
"""

import sys
if sys.version_info[0] != 3:
    print('Python 3 required.')
    sys.exit()
import curses
import random
import time
import datetime

def main():
    stdscr = set_up_curses()
    try:
        main_loop(stdscr)
    except KeyboardInterrupt:
        # If program core finished, restore terminal settings.
        curses.nocbreak() # end character-break mode.
        stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        # Destroy window.
        curses.endwin()

#        close_curses(stdscr)
#    close_curses(stdscr)


###################
# Body of program #
###################

def main_loop(stdscr):
    window = curses.newwin(curses.LINES, curses.COLS)
    start_time = time.time()
    while True:
        # Different subwindows: score_bar, main_win, defense_bar.
        t = str(datetime.timedelta(seconds=round(time.time()-start_time)))
        score = ('''Score: {:>4}  Level: {:>4}  Damage: {:>3}  '''
                '''Time remaining: {}'''.
                        format(random.randint(1, 100), random.randint(1, 100),
                        random.randint(1, 100), t))
        stdscr.addstr(0, 0, score)#, curses.A_REVERSE)
#        stdscr.chgat(-1, curses.A_REVERSE)
        stdscr.chgat(0, 0, 7, curses.color_pair(142))
        stdscr.chgat(0, 12, 7, curses.color_pair(142))
        stdscr.chgat(0, 24, 9, curses.color_pair(142))
        stdscr.chgat(0, 36, 17, curses.color_pair(142))
        stdscr.chgat(0, 7, 4, curses.color_pair(198))
        stdscr.chgat(0, 20, 4, curses.color_pair(198))
        stdscr.chgat(0, 34, 3, curses.color_pair(198))
        stdscr.chgat(0, 53, 10, curses.color_pair(198))
        # Get next character in regex string.
        c = window.getch()
        # Append to regex string and try against attack and non-combattant
        # strings.
        pass
        refresh(stdscr, window)

# Things to do:
# Find current window dimensions using window.getmaxyx()
# Set background color.
# Item gradually fading into view.
# Input box.

def refresh(stdscr, window):
    stdscr.noutrefresh()
    window.noutrefresh()
    curses.doupdate()

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
    # Declare colors.
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
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
