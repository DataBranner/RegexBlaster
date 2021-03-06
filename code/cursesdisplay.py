#! /usr/bin/python
# cursesdisplay.py
# David Prager Branner
# 20140506

import sys
import curses
import random
import time
from scorer import Scorer

class CursesDisplay():
    def __init__(self):
        self.maxlines = 30
        self.attacks_row = 2
        self.attacks_max = self.maxlines - 5
        self.bystander_row = 2
        self.bystander_max = self.maxlines - 5
        self.set_up_curses()
        self.fade_colors = {
                self.attacks: [
                197, 203, 209, 215, 221, 
                227, 228, 229, 230, 231, 232,
                255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245,
                244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233],
                self.bystander: [
                47, 48, 49, 50, 51, 52, 
                88, 124, 160, 196, 232,
                255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245,
                244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233],
                'fade in and reverse': [
#                233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 
                245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255,
                232, 231, 230, 229, 228, 227,
                221, 215, 209, 203, 197],
                }

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
        self.half_screen = curses.COLS // 2
        self.attacks = curses.newwin(curses.LINES-3, self.half_screen, 1, 0)
        self.attacks_color = curses.color_pair(197)
        self.attacks.attrset(self.attacks_color)
        self.attacks.addstr(1, 0, 'ATTACK STRINGS (MATCH THESE)'.
                center(self.half_screen, ' '), curses.A_UNDERLINE |
                self.attacks_color)
        self.attacks.box()
        self.bystander = curses.newwin(
                curses.LINES-3, self.half_screen, 1, self.half_screen)
        self.bystander_color = curses.color_pair(47)
        self.bystander.attrset(self.bystander_color)
        self.bystander.addstr(1, 0, '''BYSTANDER STRINGS (DO NOT MATCH)'''.
                center(self.half_screen, ' '), curses.A_UNDERLINE)
        self.bystander.box()

    def refresh(self):
        self.stdscr.noutrefresh()
        self.window.noutrefresh()
        self.attacks.noutrefresh()
        self.bystander.noutrefresh()
        curses.doupdate()

    def end_game(self):
        """End game cleanly, restoring terminal to working state."""
        curses.nocbreak() # end character-break mode.
        self.stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        # Destroy window.
        curses.endwin()
        sys.exit(0)

    def display_score(self, score, attacks_left, bystanders_left):
        self.score = ('''Score: {:>3}    Minimum attacks left: {:>2}    '''
                '''Maximum bystander hits left: {:>2}'''.
                format(score, attacks_left, bystanders_left))
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
        defense_line = 'Defense: ' + defense
        # Defense line appears in white (color pair 16).
        self.stdscr.addstr(
                curses.LINES-1, 0, defense_line, curses.color_pair(16))
        # Anything deleted is overwritten with blackness (color pair 1).
        self.stdscr.chgat(curses.LINES-1, len(defense_line), -1,
                curses.color_pair(1))

    def display_attacks(self, attack):
        """Display attack string."""
        # QQQ Can this and display_bystander() be merged, since func similar?
        self.attacks.addstr(
                len(attack), 1,
                attack[-1].center(self.half_screen-2, ' '))
        self.refresh()

    def display_bystander(self, bystander):
        """Display bystander string."""
        self.bystander.addstr(
                len(bystander), 1,
                bystander[-1].center(self.half_screen-2, ' '))
        self.refresh()

    def fade_out(self, object, y, x, length):
        """Make item fade out gradually.

        Intended for use with defeated attack strings.
        """
        for color in self.fade_colors[object]:
            object.chgat(y, x, length, curses.color_pair(color))
            self.refresh()
            curses.delay_output(40)
        # QQQ This should happen while other things are happening.
        # QQQ We need different fade sequence for different starting color.

    def highlight_failure(self, object, y, x, length):
        """Reverse item and turn it the color of an attack.

        Intended for use with failed attacks or bystanders hit."""
        for color in self.fade_colors['fade in and reverse']:
            object.chgat(
                    y, x, length, curses.A_REVERSE | curses.color_pair(color))
            self.refresh()
            curses.delay_output(40)
#        object.chgat(y, x, length, curses.A_REVERSE | self.attacks_color)
