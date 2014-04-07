#! /usr/bin/python
# cursesdisplay.py
# David Prager Branner
# 20140407

import curses
import random
from timer import Timer
from scorer import Scorer

class CursesDisplay():
    def __init__(self):
        self.T = Timer()
        self.S = Scorer()
        self.maxlines = 30
        self.attacks_row = 2
        self.attacks_max = self.maxlines - 5
        self.noncomb_row = 2
        self.noncomb_max = self.maxlines - 5
        self.set_up_curses()

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
        curses.resizeterm(self.maxlines, 80)
        self.window = curses.newwin(curses.LINES, curses.COLS)
        self.window.nodelay(1)
        # Create and configure main half-screen subwindows.
        self.half_screen = curses.COLS//2
        self.attacks = curses.newwin(curses.LINES-3, self.half_screen, 1, 0)
        self.attacks.attrset(curses.color_pair(198))
        self.attacks.addstr(1, 0, 'ATTACK STRINGS (KILL THESE)'.
                center(self.half_screen, ' '), curses.A_UNDERLINE |
                curses.color_pair(198))
        self.attacks.box()
        self.noncomb = curses.newwin(
                curses.LINES-3, self.half_screen, 1, self.half_screen)
        self.noncomb.attrset(curses.color_pair(47))
        self.noncomb.addstr(1, 0, '''NON-COMBATANT STRINGS (DO NOT KILL)'''.
                center(self.half_screen, ' '), curses.A_UNDERLINE)
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
        if self.T.time_left < 0:
            self.end_game()
        else:
            self.score = ('''Score: {:>4}  Level: {:>4}  Damage: {:>3}  '''
                    '''Time remaining: {:<8}'''.
                    format(self.S.score,
                        random.randint(1, 100), random.randint(1, 100),
                        self.T.time_left_str))
            self.T.update()
            self.stdscr.addstr(0, 0, self.score)
            self.stdscr.attrset(curses.color_pair(16))
            self.refresh()

    def display_message(self):
        """Display message about game state."""
        self.stdscr.addstr(
                curses.LINES-2, 0, self.S.message.rjust(80, ' '), 
                curses.color_pair(142))
        # The following was commented out when self.S.message was replaced with
        # self.S.message.rjust.
#        # Anything deleted is overwritten with blackness (color pair 1).
#        self.stdscr.chgat(curses.LINES-2, len(self.S.message), -1,
#                curses.color_pair(1))

    def display_defense(self):
        """Display user's defense string."""
        defense_line = 'defense: ' + self.S.defense
        # Defense line appears in white (color pair 16).
        self.stdscr.addstr(
                curses.LINES-1, 0, defense_line, curses.color_pair(16))
        # Anything deleted is overwritten with blackness (color pair 1).
        self.stdscr.chgat(curses.LINES-1, len(defense_line), -1,
                curses.color_pair(1))

    def display_attacks(self):
        """Display attack string."""
        # Can this and display_noncomb() be merged?
        if self.attacks_row >= self.attacks_max:
            self.end_game()
        else:
            self.attacks_row += 1
            self.attacks.addstr(
                    self.attacks_row, 1,
                    self.S.attack.center(self.half_screen-2, ' '))

    def display_noncomb(self):
        """Display noncombatant string."""
        if self.noncomb_row >= self.noncomb_max:
            self.end_game()
        else:
            self.noncomb_row += 1
            self.noncomb.addstr(
                    self.noncomb_row, 1,
                    self.S.noncombatant.center(self.half_screen-2, ' '))

    def fade_out(self):
        """Make item fade out gradually.

        Intended for use with defeated attack strings.
        """
        pass

    def highlight_failure(self):
        """Reverse item and turn it the color of an attack.

        Intended for use with failed attacks or non-combatants hit."""
        pass
