#! /usr/bin/python
# curses_tester_07.py
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
        self.defense = ''
        self.defense_submitted = ''
        self.attack = ''
        self.noncombatant = ''
        self.message = ''
        self.new_attacks = True
        self.new_noncomb = True

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
            self.message = (
                    'Successful defense without non-combatant casualties.')
            self.fade_out()
            self.defeated_attacks.append(attack)
            self.score += 1 * self.level
            self.level += .1
        elif collateral_damage:
            self.message = 'Non-combatant casualties!'
            self.highlight_failure()
            # Assess penalty
            self.score -= 1 * self.level
        if not attack_successful:
            self.message = 'Defense failed!'
            # Hit increases damage
            self.damage -= 1

    def fade_out(self):
        """Make item fade out gradually.

        Intended for use with defeated attack strings.
        """
        pass

    def highlight_failure(self):
        """Reverse item.

        Intended for use with failed attacks or non-combatants hit."""
        pass


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
        self.stdscr.addstr(
                curses.LINES-2, 0, self.S.message.rjust(80, ' '), 
                curses.color_pair(142))
        # The following was commented out when self.S.message was replaced with
        # self.S.message.rjust.
#        # Anything deleted is overwritten with blackness (color pair 1).
#        self.stdscr.chgat(curses.LINES-2, len(self.S.message), -1,
#                curses.color_pair(1))

    def display_defense(self):
        defense_line = 'defense: ' + self.S.defense
        # Defense line appears in white (color pair 16).
        self.stdscr.addstr(
                curses.LINES-1, 0, defense_line, curses.color_pair(16))
        # Anything deleted is overwritten with blackness (color pair 1).
        self.stdscr.chgat(curses.LINES-1, len(defense_line), -1,
                curses.color_pair(1))

    def display_attacks(self):
        if self.attacks_row >= self.attacks_max:
            self.end_game()
        else:
            self.attacks_row += 1
            self.attacks.addstr(
                    self.attacks_row, 1,
                    self.S.attack.center(self.half_screen-2, ' '))

    def display_noncomb(self):
        if self.noncomb_row >= self.noncomb_max:
            self.end_game()
        else:
            self.noncomb_row += 1
            self.noncomb.addstr(
                    self.noncomb_row, 1,
                    self.S.noncombatant.center(self.half_screen-2, ' '))


def main():
    cd = CursesDisplay()
    try:
        main_loop(cd)
    except KeyboardInterrupt:
        # If program core finished, restore terminal settings.
        curses.nocbreak() # end character-break mode.
        cd.stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        # Destroy window.
        curses.endwin()

###################
# Body of program #
###################

def main_loop(cd):
    while cd.S.damage > 0:
        curses.delay_output(10)
        cd.display_score()
        cd.display_message()
        cd.display_defense()
        attack_defend_cycle(cd)
    if cd.S.damage <= 0:
        cd.S.message = 'Your player has been destroyed in battle. Game over.'

#######################
# End of program body #
#######################

def attack_defend_cycle(cd):
    # Generate "attack" string (must be matched to avoid hit)
    if cd.S.new_attacks:
        cd.S.new_attacks = False
        cd.S.attack = generate_string()
        cd.display_attacks()
    # Generate "noncombatant" string (must be matched to avoid score-loss)
    if cd.S.new_noncomb:
        cd.S.new_noncomb = False
        cd.S.noncombatant = generate_string()
        cd.display_noncomb()
    #
    # Battle state loop.
    # Get next character in regex string.
    try:
        c = cd.window.getch()
        # Delete last character: DEL, BS.
        if c in {127, 18}:
            cd.S.defense = cd.S.defense[:-1]
        # Submit finished string: CR, LF, VT, FF, ESC.
        elif c in {10, 13, 11, 12, 27}:
            # Clear message and submit handle completed defense string.
            cd.S.message = ''
            cd.S.defense_submitted = cd.S.defense
        # Other control characters. QQQ we have not dealt with arrow keys.
        elif c == -1 or not (32 <= c <= 126):
            pass
        # For checking other delete characters, use cd.S.defense += str(c)
        else:
#            cd.S.defense += str(c)
            cd.S.defense += chr(c)
    except ValueError:
        pass
    # Append to regex string and try against attack and non-combatant strings.
    # Two components: 
    #    Finished defense string is passed to assess_defense_single; 
    #    Unfinished defense string is, if possible, evaluated tentatively 
    #        against attack and noncombatant strings.
    if cd.S.defense_submitted:
        self.new_attacks = True
        self.new_noncomb = True
        attack_successful, collateral_damage = (
                cd.S.assess_defense_single(
                    cd.S.defense_submitted, cd.S.attack, cd.S.noncombatant))
        # Check defense against past regexes; invalidate if found.
        if cd.S.defense_submitted in cd.S.defense_record:
            cd.S.message = 'This defense has already been used; invalid.'
        else:
            cd.S.defense_record.add(cd.S.defense_submitted)
            cd.S.defense_submitted = ''

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
