#! /usr/bin/python
# curses_tester_03.py
# David Prager Branner
# 20140402

"""Explore the use of Ncurses.

04 Set up different sub-windows. Separate Timer class. Defense line.
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

class Timer():
    def __init__(self, time_limit=10):
        self.start_time = time.time()
        self.time_limit = time_limit
        self.update()

    def update(self):
        self.time_passed = time.time() - self.start_time
        self.time_left = self.time_limit - self.time_passed
        self.time_left_str = str(
                datetime.timedelta(seconds=round(self.time_left))) 
        if self.time_left_str[0:5] == '0:00:':
            self.time_left_str = self.time_left_str[5:]
        elif self.time_left_str[0:2] == '0:':
            self.time_left_str = self.time_left_str[2:]
        if self.time_left_str[0] == '0':
            self.time_left_str = self.time_left_str[1:]


class Window():
    def __init__(self):
        self.set_up_curses()
        self.timer = Timer()
        self.score = None
        self.defense = ''

    def set_up_curses(self):
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
        # Create and configure window.
        self.window = curses.newwin(curses.LINES, curses.COLS)
        self.window.chgat(curses.color_pair(198))
        self.window.nodelay(1)
        # Create and configure main half-screen subwindows.
        half_screen = curses.COLS//2
        self.attacks = curses.newwin(curses.LINES-3, half_screen, 1, 0)
        self.attacks.box()
        self.noncomb = curses.newwin(
                curses.LINES-3, half_screen, 1, half_screen)
        self.noncomb.chgat(-1, curses.color_pair(198))
        self.noncomb.box()

    def refresh(self):
        self.stdscr.noutrefresh()
        self.window.noutrefresh()
        self.attacks.noutrefresh()
        self.noncomb.noutrefresh()
        curses.doupdate()

    def end_game(self):
        self.window.nodelay(0)

    def display_score(self):
        if self.timer.time_left < 0:
            self.end_game()
        else:
            self.score = ('''Score: {:>4}  Level: {:>4}  Damage: {:>3}  '''
                    '''Time remaining: {:<8}'''.
                            format(random.randint(1, 100),
                                random.randint(1, 100), random.randint(1, 100),
                                self.timer.time_left_str))
            self.timer.update()
            self.stdscr.addstr(0, 0, self.score)
            self.stdscr.chgat(0, 0, -1, curses.color_pair(142)) # Score
            self.stdscr.chgat(0, 7, -1, curses.color_pair(198))
            self.stdscr.chgat(0, 12, -1, curses.color_pair(142)) # Level
            self.stdscr.chgat(0, 20, -1, curses.color_pair(198))
            self.stdscr.chgat(0, 24, -1, curses.color_pair(142)) # Damage
            self.stdscr.chgat(0, 34, -1, curses.color_pair(198))
            self.stdscr.chgat(0, 38, -1, curses.color_pair(142)) #Time remaining
            self.stdscr.chgat(0, 53, -1, curses.color_pair(198))
            self.refresh()

    def display_message(self):
        pass

    def display_defense(self):
        defense_line = 'defense: ' + self.defense
        # Defense line appears in white (color pair 16).
        self.stdscr.addstr(
                curses.LINES-1, 0, defense_line, curses.color_pair(16))
        # Anything deleted is overwritten with blackness (color pair 1).
        self.stdscr.chgat(curses.LINES-1, len(defense_line), -1,
                curses.color_pair(1))

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
    while True:
        # Different subwindows: scores, main window, messages, defense-strings..
        # Add code only to update every second or on change.
        curses.delay_output(100)
        w.display_score()
        w.display_message()
        w.display_defense()
        # Get next character in regex string.
        try:
            c = w.window.getch()
            if c == 127:
                w.defense = w.defense[:-1]
#            w.defense += str(c)
            else:
                w.defense += chr(c)
        except ValueError:
            pass
        # Append to regex string and try against attack and non-combatant
        # strings. Must display what we have in special window, so user seems
        # to be typing into window.
        pass

# Things to do:
# Find current window dimensions using window.getmaxyx(). Revisit this.
# Set background color: automatically black for now.
# Item gradually fading into or out of view. Useful for hits.

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
