#! /usr/bin/python
# scorer.py
# David Prager Branner
# 20140407

import re
import random # used only for dummy values


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
        self.attack_y = 0
        self.attack_x = 0
        self.noncombatant = ''
        self.noncomb_y = 0
        self.noncomb_x = 0
        self.message = ''
        self.new_attacks = True
        self.new_noncomb = True
        self.attack_successful = None
        self.collateral_damage = None

    def assess_defense_single(self):
        """Determine success, side-effects of defense in single-attack event."""
        # Attack; later we need to be able to handle multiple attacks.
        self.attack_successful = False
        try:
            match = re.search(self.defense, self.attack).group()
        except AttributeError or TypeError:
            match = None
        if self.attack == match:
            self.attack_successful = True
        # Non-targets (penalty for hitting); later need to handle multiple.
        self.collateral_damage = False
        try:
            match = re.search(self.defense, self.noncombatant).group()
        except AttributeError or TypeError:
            match = None
        if self.noncombatant == match:
            self.collateral_damage = True

    def score_defense(self):
        """Update score, damage, and level based on defense results."""
        if self.attack_successful and not self.collateral_damage:
            # Defeat attack
            self.message = (
                    'Successful defense without non-combatant casualties.')
#            self.fade_out(self.attack_y_x, self.attack)
            self.defeated_attacks.append(self.attack)
            self.score += round(self.level, 2) # QQQ call evaluate_defense()
            self.level += .1
        elif self.collateral_damage:
            self.message = 'Non-combatant casualties!'
#            self.highlight_failure()
            # Assess penalty
            self.score -= self.level # QQQ call evaluate_defense()
        if not self.attack_successful:
            self.message = 'Defense failed!'
#            self.highlight_failure()
            # Hit increases damage
            self.damage -= 1

    def evaluate_defense(self):
        """Check for presence of scoreable operators and grade accordingly."""
        pass