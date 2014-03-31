#!/usr/bin/python3
# blaster.py
# David Prager Branner
# 20140330

"""Game to improve regex skills.

Computer generates "attack" string and possibly "noncombatant" string.

User generates "defense" regex pattern; must match "attack" but not
"noncombatant".
"""

import re
import random
import string

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
        except AttributeError:
            match = None
        if attack == match:
            attack_successful = True
        # Non-targets (penalty for hitting); later need to handle multiple.
        collateral_damage = False
        try:
            match = re.search(defense, noncombatant).group()
        except AttributeError:
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


def main():
    s = Scorer()
    while s.damage > 0:
        defense = None
        # Generate "attack" string (must be matched to avoid hit)
        attack = generate_string()
        # Generate "noncombatant" string (must be matched to avoid score-loss)
        noncombatant = generate_string()
        # Battle state loop.
        defense = report_battle_state(s, defense, attack, noncombatant)
        # Test defense against "attack" and "noncombatant".
        attack_successful, collateral_damage = (
                s.assess_defense_single(defense, attack, noncombatant))
        s.score_defense(attack, attack_successful, collateral_damage)
    if s.damage <= 0:
        print('\nYour player has been destroyed in battle. Game over.')

def report_battle_state(s, defense, attack, noncombatant):
    while True:
        # Report battle state.
        print('''Score {:>4.1f} Level {:>4.1f} Damage {:>4.1f} '''
                '''Attack {:>10} Non-c {:>10}'''.format(s.score, s.level, 
                    s.damage, attack, noncombatant), end='')
        # Collect "defense" (user regex).
        defense = input(' load: ')
        # Check defense against past regexes; invalidate if found.
        if defense in s.defense_record:
            print('This defense has already been used.')
            continue
        else:
            s.defense_record.add(defense)
            return defense

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
