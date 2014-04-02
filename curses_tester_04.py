#! /usr/bin/python
# curses_tester_03.py
# David Prager Branner
# 20140402

"""Explore the use of Ncurses.

04 Set up different sub-windows.
03 Get styled text working; no display delay on startup..
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

class Window():
    def __init__(self):
        self.set_up_curses()

    def set_up_curses(self):
        self.score = None
        # Instantiate standard screen object.
        self.stdscr = curses.initscr()
        # Properly initialize screen.
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        # Check for and begin color support.
        if curses.has_colors():
            curses.start_color()
        # Optionally enable the F-1 etc. keys, which are multi-byte.
        self.stdscr.keypad(1)
        # Declare colors.
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.window = curses.newwin(curses.LINES, curses.COLS)
        self.window.nodelay(1)

    def refresh(self):
        self.stdscr.noutrefresh()
        self.window.noutrefresh()
        curses.doupdate()

    def end_game(self):
        self.window.nodelay(0)

    def display_score(self):
        self.stdscr.addstr(0, 0, self.score)#, curses.A_REVERSE)
        self.stdscr.chgat(0, 0, -1, curses.color_pair(142)) # Score
        self.stdscr.chgat(0, 7, -1, curses.color_pair(198))
        self.stdscr.chgat(0, 12, -1, curses.color_pair(142)) # Level
        self.stdscr.chgat(0, 20, -1, curses.color_pair(198))
        self.stdscr.chgat(0, 24, -1, curses.color_pair(142)) # Damage
        self.stdscr.chgat(0, 34, -1, curses.color_pair(198))
        self.stdscr.chgat(0, 38, -1, curses.color_pair(142)) # Time remaining
        self.stdscr.chgat(0, 53, -1, curses.color_pair(198))
        self.refresh()

def main():
    w = Window()
    try:
        main_loop(w)
    except KeyboardInterrupt:
        # If program core finished, restore terminal settings.
        curses.nocbreak() # end character-break mode.
        w.stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        # Destroy window.
        curses.endwin()

###################
# Body of program #
###################

def main_loop(w):
    start_time = time.time()
    time_limit = 10
    while True:
        # Different subwindows: score_bar, main_win, defense_bar.
        time_passed = time.time() - start_time
        time_left = time_limit - time_passed
        if time_left < 0:
            w.end_game()
        time_left = str(datetime.timedelta(seconds=round(time_left)))
        if time_left[0:5] == '0:00:':
            time_left = time_left[5:]
        elif time_left[0:2] == '0:':
            time_left = time_left[2:]
        if time_left[0] == '0':
            time_left = time_left[1:]
        w.score = ('''Score: {:>4}  Level: {:>4}  Damage: {:>3}  '''
                '''Time remaining: {:<8}'''.
                        format(random.randint(1, 100), random.randint(1, 100),
                        random.randint(1, 100), time_left))
        # Add code only to update every second or on change.
        curses.delay_output(100)
        w.display_score()
        # Get next character in regex string.
        c = w.window.getch()
        # Append to regex string and try against attack and non-combatant
        # strings.
        pass

# Things to do:
# Find current window dimensions using window.getmaxyx()
# Set background color.
# Item gradually fading into view.
# Input box.

#######################
# End of program body #
#######################

#######################
# Curses housekeeping #
#######################


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
