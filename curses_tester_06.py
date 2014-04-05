#! /usr/bin/python
# curses_tester_06.py
# David Prager Branner
# 20140405

"""Arcade game to help user practice regular expressions. Curses version."""

import sys
# Not necessary: appears to work in Python 2.
#if sys.version_info[0] != 3:
#    print('Python 3 required.')
#    sys.exit()
import curses
import random
import time
import datetime
import re
import string

class Timer():
    def __init__(self, time_limit=30):
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


class Scorer():
    def __init__(self):
        self.score = 0
        self.level = 1
        self.damage = 10
        self.defense_record = set()
        self.defeated_attacks = []
        self.martyred_noncombatants = []

    def assess_defense_single(self, defense, attack, noncombatant):
        """Determine success, side-effects of defense in single-attack event."""
        # Attack; later we need to be able to handle multiple attacks.
        attack_successful = False
        try:
            match = re.search(defense, attack).group()
        except AttributeError or TypeError:
            match = None
        if attack == match:
            attack_successful = True
        # Non-targets (penalty for hitting); later need to handle multiple.
        collateral_damage = False
        try:
            match = re.search(defense, noncombatant).group()
        except AttributeError or TypeError:
            match = None
        if noncombatant == match:
            collateral_damage = True
        return attack_successful, collateral_damage

    def score_defense(self, attack, attack_successful, collateral_damage):
        """Update score, damage, and level based on defense results."""
        if attack_successful and not collateral_damage:
            # Defeat attack
            print('Successful defense without non-combatant casualties.')
            self.defeated_attacks.append(attack)
            self.score += 1 * self.level
            self.level += .1
        elif collateral_damage:
            print('Non-combatant casualties!')
            # Assess penalty
            self.score -= 1 * self.level
        if not attack_successful:
            print('Defense failed!')
            # Hit increases damage
            self.damage -= 1

    def advance_fade_out(self):
        pass


class Window():
    def __init__(self):
        self.set_up_curses()
        self.T = Timer()
        self.S = Scorer()
        self.defense = ''
        self.defense_submitted = ''
        self.message = ''

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
        curses.resizeterm(30, 80)
        self.window = curses.newwin(curses.LINES, curses.COLS)
        self.window.nodelay(1)
        # Create and configure main half-screen subwindows.
        half_screen = curses.COLS//2
        self.attacks = curses.newwin(curses.LINES-3, half_screen, 1, 0)
        self.attacks.attrset(curses.color_pair(198))
        self.attacks.addstr(1, 0, 'ATTACK STRINGS (KILL THESE)'.
                center(half_screen, ' '))
        self.attacks.box()
        self.noncomb = curses.newwin(
                curses.LINES-3, half_screen, 1, half_screen)
        self.noncomb.attrset(curses.color_pair(47))
        self.noncomb.addstr(1, 0, '''NON-COMBATANT STRINGS (DO NOT KILL)'''.
                center(half_screen, ' '))
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
#            self.stdscr.chgat(0, 0, -1, curses.color_pair(142)) # Score
#            self.stdscr.chgat(0, 7, -1, curses.color_pair(198))
#            self.stdscr.chgat(0, 12, -1, curses.color_pair(142)) # Level
#            self.stdscr.chgat(0, 20, -1, curses.color_pair(198))
#            self.stdscr.chgat(0, 24, -1, curses.color_pair(142)) # Damage
#            self.stdscr.chgat(0, 34, -1, curses.color_pair(198))
#            self.stdscr.chgat(0, 38, -1, curses.color_pair(142)) #Time remaining
#            self.stdscr.chgat(0, 53, -1, curses.color_pair(198))
            self.refresh()

    def display_message(self):
        self.stdscr.addstr(
                curses.LINES-2, 0, self.message.rjust(80, ' '), 
                curses.color_pair(142))
        # The following was commented out when self.message was replaced with
        # self.message.rjust.
#        # Anything deleted is overwritten with blackness (color pair 1).
#        self.stdscr.chgat(curses.LINES-2, len(self.message), -1,
#                curses.color_pair(1))

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
    while w.S.damage > 0:
        # Different subwindows: scores, main window, messages, defense-strings.
        # Add code only to update every second or on change.
        curses.delay_output(10)
        w.display_score()
        w.display_message()
        w.display_defense()
        attack_defend_cycle(w)
    if w.S.damage <= 0:
        w.message = 'Your player has been destroyed in battle. Game over.'

#######################
# End of program body #
#######################

def attack_defend_cycle(w):
    # Generate "attack" string (must be matched to avoid hit)
    attack = generate_string()
    # Generate "noncombatant" string (must be matched to avoid score-loss)
    noncombatant = generate_string()
    # Battle state loop.
    # Get next character in regex string.
    try:
        c = w.window.getch()
        # Delete last character: DEL, BS.
        if c in {127, 18}:
            w.defense = w.defense[:-1]
        # Submit finished string: CR, LF, VT, FF, ESC.
        elif c in {10, 13, 11, 12, 27}:
            # Clear message and submit handle completed defense string.
            w.message = ''
            w.defense_submitted = w.defense # qqq add defense_submitted to W
        # Other control characters. QQQ we have not dealt with arrow keys.
        elif c == -1 or not (32 <= c <= 126):
            pass
        # For checking other delete characters, use w.defense += str(c)
        else:
#            w.defense += str(c)
            w.defense += chr(c)
    except ValueError:
        pass
    # Append to regex string and try against attack and non-combatant strings.
    # Two components: 
    #    Finished defense string is passed to assess_defense_single; 
    #    Unfinished defense string is, if possible, evaluated tentatively 
    #        against attack and noncombatant strings.
    if w.defense_submitted:
        attack_successful, collateral_damage = (
                w.S.assess_defense_single(
                    w.defense_submitted, attack, noncombatant))
        # Check defense against past regexes; invalidate if found.
        if w.defense_submitted in w.S.defense_record:
            w.message = 'This defense has already been used; invalid.'
        else:
            w.S.defense_record.add(w.defense_submitted)
            w.defense_submitted = ''

charset_dict = {
        'a': string.ascii_lowercase,
        'A': string.ascii_uppercase,
        '0': string.digits,
        '.': string.punctuation,
        }
 
def choose_charset(typestring='aA'):
    charset = ''
    for item in typestring:
        if item == ' ':
            continue
        charset += charset_dict[item]
    # Spaces must follow all others since their numbers are proportional.
    if ' ' in typestring:
        charset += ' ' * (len(charset) // 2)
    return charset
 
def generate_string(length=5, typestring='aA', varying=False):
    if varying:
        # Must call a more complicated function, not yet written
        pass
    charset = choose_charset(typestring)
    return ''.join([random.choice(charset) for i in range(length)])             

if __name__ == '__main__':
    main()
