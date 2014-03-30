#!/usr/bin/python3
# blaster.py
# David Prager Branner
# 20140328

"""Game to improve regex skills.

Computer generates "attack" string and possibly "noncombatant" string.

User generates "defense" regex pattern; must match "attack" but not
"noncombatant".
"""

# For later:
#  1. Handle near-identical defenses:
#   a. evaluate by edit-distance vis-à-vis all previous defenses; average
#      string-length minus edit-distance may be more useful than
#      edit-distance alone.
#   b. handle by repeating attack string; repeat defense barred;
#   c. handle by delaying efficacy, thus increasing risk of hit (San's
#      suggestion); this requires implementing timing.
#  2. Generate progressively more complex attack strings. There are presumably
#     ways to do this formulaically. We should also try to create noncombatant
#     strings and attack strings in such a way as to be difficult to
#     distinguish.
#  3. In future we may want multiple attack and/or noncombatant strings.
#  4. Invalid defense string may lead to score reduction or other penalties.
#  5. Evaluate quality of defense for more scores or greater level increase.
#  6. Figure damage (from hits); it may affect time of defense's effect..
#  7. For more complex attacks, it may be interesting to repeat them just in
#     order to see how many different defenses the user can supply. Keep
#     repeating until user fails — or even a little after that.
#  8. If \w appears a lot, add whitespace.

import re
import random
import string

def main():
    # Set up variables
    score = 0
    level = 1
    damage = 10
    defense_record = set()
    defeated_attacks = []
    martyred_noncombatants = []
    while damage > 0:
        defense = None
        # Generate "attack" string (must be matched to avoid hit)
        attack = generate_string()
        # Generate "noncombatant" string (must be matched to avoid score-loss)
        noncombatant = generate_string()
        while True:
            # Report battle state.
            print('''Score {:>4.1f} Level {:>4.1f} Damage {:>4.1f} '''
                    '''Attack {:>10} Non-c {:>10}'''.
                    format(score, level, damage, attack, noncombatant), end=' ')
            # Collect "defense" (user regex).
            defense = input('load: ')
            # Check defense against past regexes; invalidate if found.
            if defense in defense_record:
                print('This defense has already been used.')
                continue
            else:
                defense_record.add(defense)
                break
        # Test defense against "attack" and "noncombatant".
        attack_successful, collateral_damage = (
                assess_defense(defense, attack, noncombatant))
        if attack_successful and not collateral_damage:
            # Defeat attack
            print('Successful defense without non-combatant casualties.')
            defeated_attacks.append(attack)
            score += 1 * level
            level += .1
        elif collateral_damage:
            print('Non-combatant casualties!')
            # Assess penalty
            score -= 1 * level
        if not attack_successful:
            print('Defense failed!')
            # Hit increases damage
            damage -= 1

def assess_defense_single(defense, attack, noncombatant):
    """Determine success of defense and collaterals in single-attack event."""
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
    if attack == match:
        collateral_damage = True
    return attack_successful, collateral_damage

def choose_charset(typestring=''):
    charset = ''
    if 'a' in typestring:
        charset += string.ascii_lowercase
    if 'A' in typestring:
        charset += string.ascii_uppercase
    if '0' in typestring:
        charset += string.digits

def generate_string(length=5, typestring='aA'):
    if 'a' in typestring:

    return ''.join([random.choice(string.ascii_letters) for i in range(length)])
