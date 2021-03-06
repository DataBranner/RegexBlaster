#! /usr/bin/python
# regex_blaster_15.py
# David Prager Branner
# 20140506

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
import stringmaker
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
        cd.end_game()
        # If ctrl-c, restore terminal settings.
#        curses.nocbreak() # end character-break mode.
#        cd.stdscr.keypad(0)
#        curses.echo()
#        curses.curs_set(1)
        # Destroy window.
#        curses.endwin()

###################
# Body of program #
###################

def main_loop(cd):
    """Endless loop until maximum failed defenses or non-comb death occurs."""
    # S.attack_limit > len(S.attack) because we need only the minimum failed
    #     defenses.
    S.message = ('Quit at any time with the ESC key.')
    cd.display_message(S.message)
    while (S.attack_limit > len(S.attack) and
            S.attack_limit > len(S.bystander)):
        if T.time_limit and T.time_to_display < 0:
            cd.end_game()
        else:
            # Somewhere in this cycle the number of bystanders left is wrong.
            T.update()
            curses.delay_output(10)
            cd.display_defense(S.defense)
            attack_defend_cycle()
            cd.display_message(S.message)
            cd.display_score(S.score,
                    S.attack_limit-len(S.attack),
                    S.attack_limit-len(S.bystander))
#            cd.refresh() # this causes problems
    S.message = ('''Your player has been destroyed in battle. Game over.''')
    cd.display_message(S.message)
#    curses.delay_output(4000)
    cd.stdscr.noutrefresh()
    curses.doupdate()
#    cd.end_game()

#######################
# End of program body #
#######################

def attack_defend_cycle():
    # Generate "attack" string (must be matched to avoid hit)
    if S.new_attacks:
        S.new_attacks = False
        if S.invalid_defense:
            string = S.attack[-1]
        else:
            string = generate_string()
        S.attack.append(string)
        cd.display_attacks(S.attack)
        # Prepare for next cycle.
        S.invalid_defense = False
    # Generate "bystander" string (must be matched to avoid score-loss)
    if S.new_bystander:
        S.new_bystander = False
        S.bystander.append(generate_string())
        cd.display_bystander(S.bystander)
    #
    # Battle state loop.
    # Get next character in regex string.
    try:
        c = cd.window.getch() # Non-blocking, because cd.window.nodelay(1) set.
    except ValueError:
        pass
    # Delete last character: DEL, BS.
    if c in {127, 18}:
        S.defense = S.defense[:-1]
    # Submit finished string: CR, LF, VT, FF.
    elif c in {10, 13, 11, 12}:
        # Clear message and submit handle completed defense string.
        S.message = ''
        S.defense_submitted = S.defense
    # Quit game: ESC.
    elif c == 27:
        # Restore terminal settings.
        curses.nocbreak() # end character-break mode.
        cd.stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        # Destroy window.
        curses.endwin()
        sys.exit(0)
    # Other control characters. QQQ we have not dealt with arrow keys.
    elif c == -1 or not (32 <= c <= 126):
        pass
    # For checking other delete characters, use S.defense += str(c)
    else:
        S.defense += chr(c)
    # Append to regex string and try against attack and bystander strings.
    # Two components:
    #    Finished defense string is passed to assess_defense_single;
    #    Unfinished defense string is, if possible, evaluated tentatively
    #        against attack and bystander strings. (Not yet done. QQQ)
    if S.defense_submitted:
        S.after_defense_is_submitted()
        cd.refresh()
        if S.attack_successful:
            # Fade and remove attack.
            cd.fade_out(
                    cd.attacks, len(S.attack), 1, cd.half_screen-2)
        else:
            cd.highlight_failure(
                    cd.attacks, len(S.attack), 1, cd.half_screen-2)
        if S.collateral_damage:
            cd.highlight_failure(
                    cd.bystander, len(S.bystander), 1, cd.half_screen-2)
        else:
            # Fade and remove bystander.
            cd.fade_out(
                    cd.bystander, len(S.bystander), 1, cd.half_screen-2)
        S.delete_used_up_strings()

choices = [
        stringmaker.make_word,
        stringmaker.make_run,
        stringmaker.make_long_string,
        ]

def generate_string():
    string = choices[(S.level // 3) % 3]()
    return string

if __name__ == '__main__':
    main()
