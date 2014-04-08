#! /usr/bin/python
# regex_blaster_08.py
# David Prager Branner
# 20140407

"""Arcade game to help user practice regular expressions. Curses version."""

import sys
# Not necessary: appears to work in Python 2.
#if sys.version_info[0] != 3:
#    print('Python 3 required.')
#    sys.exit()
import curses
import random
import string
import traceback
from cursesdisplay import CursesDisplay
from timer import Timer
from scorer import Scorer

cd = CursesDisplay()
attack_limit = cd.attacks_max
T = Timer()
S = Scorer(attack_limit)

def main():
    try:
        main_loop(cd)
    except KeyboardInterrupt:
        # If ctrl-c, restore terminal settings.
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
    while S.attack_limit > 0:
        if T.time_limit and T.time_to_display < 0:
            cd.end_game()
        else:
            T.update()
            curses.delay_output(10)
            cd.display_score(S.score, T.time_to_display_str, S.attack_limit)
            cd.display_message(S.message)
            cd.display_defense(S.defense)
            attack_defend_cycle(cd)
    if S.attack_limit <= 0:
        S.message = ('''Your player has been destroyed in battle. '''
                '''Game over; ctrl-c to quit.''')
        cd.display_message(S.message)
        cd.refresh()

#######################
# End of program body #
#######################

def attack_defend_cycle(cd):
    # Generate "attack" string (must be matched to avoid hit)
    if S.new_attacks:
        S.new_attacks = False
        S.attack = generate_string()
        cd.display_attacks(S.attack)
    # Generate "noncombatant" string (must be matched to avoid score-loss)
    if S.new_noncomb:
        S.new_noncomb = False
        S.noncombatant = generate_string()
        cd.display_noncomb(S.noncombatant)
    #
    # Battle state loop.
    # Get next character in regex string.
    try:
        c = cd.window.getch()
        # Delete last character: DEL, BS.
        if c in {127, 18}:
            S.defense = S.defense[:-1]
        # Submit finished string: CR, LF, VT, FF, ESC.
        elif c in {10, 13, 11, 12, 27}:
            # Clear message and submit handle completed defense string.
            S.message = ''
            S.defense_submitted = S.defense
        # Other control characters. QQQ we have not dealt with arrow keys.
        elif c == -1 or not (32 <= c <= 126):
            pass
        # For checking other delete characters, use S.defense += str(c)
        else:
#            S.defense += str(c)
            S.defense += chr(c)
    except ValueError:
        pass
    # Append to regex string and try against attack and non-combatant strings.
    # Two components: 
    #    Finished defense string is passed to assess_defense_single; 
    #    Unfinished defense string is, if possible, evaluated tentatively 
    #        against attack and noncombatant strings.
    if S.defense_submitted:
        # Check defense against past regexes; invalidate if found.
        if S.defense_submitted in S.defense_record:
            S.message = 'This defense has already been used; invalid.'
        else:
            S.new_attacks = True
            S.new_noncomb = True
            S.defense_record.add(S.defense_submitted)
            # Evaluate defense.
            S.assess_defense_single()
            S.defense_submitted = ''
            # Act on attack_successful, collateral_damage
            S.score_defense()
            S.defense = ''
            if S.attack_successful and not S.collateral_damage:
                # Fade attack. 
                cd.fade_out(
                        cd.attacks, cd.attacks_row, 1, cd.half_screen-2)
                if cd.attacks_row > 2:
                    cd.attacks_row -= 1
                cd.noncomb_row -= 1
            elif S.collateral_damage:
                cd.highlight_failure(
                        cd.noncomb, cd.noncomb_row, 1, cd.half_screen-2)
            elif not S.attack_successful:
                cd.highlight_failure(
                        cd.attacks, cd.attacks_row, 1, cd.half_screen-2)

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
