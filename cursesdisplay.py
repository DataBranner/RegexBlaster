#! /usr/bin/python
# cursesdisplay.py
# David Prager Branner
# 20140408

import curses
import random
from scorer import Scorer

class CursesDisplay():
    def __init__(self):
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
        self.attacks_color = curses.color_pair(198)
        self.attacks.attrset(self.attacks_color)
        self.attacks.addstr(1, 0, 'ATTACK STRINGS (KILL THESE)'.
                center(self.half_screen, ' '), curses.A_UNDERLINE |
                self.attacks_color)
        self.attacks.box()
        self.noncomb = curses.newwin(
                curses.LINES-3, self.half_screen, 1, self.half_screen)
        self.noncomb_color = curses.color_pair(47)
        self.noncomb.attrset(self.noncomb_color)
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
        self.refresh()
        self.window.nodelay(0)

    def display_score(self, score, time, attack_limit):
        self.score = ('''Score: {:>4}  Level: {:>4}  '''
                '''Attacks remaining: {:>3}  Time: {:<8}'''.
                format(score,
                    random.randint(1, 100), attack_limit, time))
        self.stdscr.addstr(0, 0, self.score)
        self.stdscr.attrset(curses.color_pair(16))
        self.refresh()

    def display_message(self, message):
        """Display message about game state."""
        self.stdscr.addstr(
                curses.LINES-2, 0, message.rjust(80, ' '), 
                curses.color_pair(142))

    def display_defense(self, defense):
        """Display user's defense string."""
        defense_line = 'defense: ' + defense
        # Defense line appears in white (color pair 16).
        self.stdscr.addstr(
                curses.LINES-1, 0, defense_line, curses.color_pair(16))
        # Anything deleted is overwritten with blackness (color pair 1).
        self.stdscr.chgat(curses.LINES-1, len(defense_line), -1,
                curses.color_pair(1))

    def display_attacks(self, attack):
        """Display attack string."""
        # QQQ Can this and display_noncomb() be merged, since func similar?
        if self.attacks_row >= self.attacks_max:
            self.end_game()
        else:
            self.attacks_row += 1
            attack = str(self.attacks_row) + ' ' + attack
            self.attacks.addstr(
                    self.attacks_row, 1,
                    attack.center(self.half_screen-2, ' '))

    def display_noncomb(self, noncombatant):
        """Display noncombatant string."""
        if self.noncomb_row >= self.noncomb_max:
            self.end_game()
        else:
            self.noncomb_row += 1
            self.noncomb.addstr(
                    self.noncomb_row, 1,
                    noncombatant.center(self.half_screen-2, ' '))

    def fade_out(self, object, y, x, length):
        """Make item fade out gradually.

        Intended for use with defeated attack strings.
        """
        fade_colors = [
                197, 203, 209, 215, 221, 227, 228, 229, 230, 231, 232,
                255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245,
                244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233]
        for color in fade_colors:
            object.chgat(y, x, length, curses.color_pair(color))
            self.refresh()
            curses.delay_output(40)
        # QQQ this should happen while other things are happening.

    def highlight_failure(self, object, y, x, length):
        """Reverse item and turn it the color of an attack.

        Intended for use with failed attacks or non-combatants hit."""
        object.chgat(y, x, length, curses.A_REVERSE | self.attacks_color)
