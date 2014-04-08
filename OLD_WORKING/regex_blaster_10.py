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
from cursesdisplay import CursesDisplay

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
        # Check defense against past regexes; invalidate if found.
        if cd.S.defense_submitted in cd.S.defense_record:
            cd.S.message = 'This defense has already been used; invalid.'
        else:
            cd.S.new_attacks = True
            cd.S.new_noncomb = True
            cd.S.defense_record.add(cd.S.defense_submitted)
            # Evaluate defense.
            cd.S.assess_defense_single()
            cd.S.defense_submitted = ''
            # Act on attack_successful, collateral_damage
            cd.S.score_defense()
            cd.S.defense = ''
            if cd.S.attack_successful and not cd.S.collateral_damage:
                # Fade attack. 
                cd.fade_out(
                        cd.attacks, cd.attacks_row, 1, cd.half_screen-2)
                if cd.attacks_row > 2:
                    cd.attacks_row -= 1
                cd.noncomb_row -= 1
            elif cd.S.collateral_damage:
                cd.highlight_failure(
                        cd.noncomb, cd.noncomb_row, 1, cd.half_screen-2)
            elif not cd.S.attack_successful:
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
