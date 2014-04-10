#! /usr/bin/python
# scorer.py
# David Prager Branner
# 20140410

import re
import random # used only for dummy values


class Scorer():
    def __init__(self, attack_limit=25):
        self.score = 0
        self.level = 1
        self.attack_limit = attack_limit
        self.defense_record = set()
        self.defeated_attacks = []
        self.martyred_bystanders = []
        self.defense = ''
        self.invalid_defense = False
        self.defense_submitted = ''
        self.attack = [None, None]
        self.bystander = [None, None]
        self.message = ''
        self.new_attacks = True
        self.new_bystander = True
        self.attack_successful = None
        self.collateral_damage = None

    def assess_cycle(self):
        """Determine success, side-effects of defense in single-attack event."""
        # Attack; later we need to be able to handle multiple attacks.
        self.attack_successful = False
        try:
            match = re.search(self.defense, self.attack[-1]).group()
        except AttributeError or TypeError:
            match = None
        if self.attack[-1] == match and not self.invalid_defense:
            self.attack_successful = True
        # Non-targets (penalty for hitting); later need to handle multiple.
        self.collateral_damage = False
        try:
            match = re.search(self.defense, self.bystander[-1]).group()
        except AttributeError or TypeError:
            match = None
        if self.bystander[-1] == match:
            self.collateral_damage = True


    def score_defense(self):
        """Update score, damage, and level based on defense results."""
        if self.attack_successful and not self.collateral_damage:
            # Gain the number of points calculated by evaluate_defense.
            self.message = (
                    'Successful defense without bystander casualties.')
            self.defeated_attacks.append(self.attack[-1])
            self.evaluate_defense(score_change='plus')
            self.level += 1
        else:
            # Lose the number of points calculated by evaluate_defense.
            self.evaluate_defense(score_change='minus')
            if self.collateral_damage and not self.invalid_defense:
                self.message = 'Bystander casualties!'
            if not self.attack_successful and not self.invalid_defense:
                self.message = 'Defense failed!'

    def delete_used_up_strings(self):
        self.defense_submitted = ''
        self.defense = ''
        if self.attack_successful:
            del self.attack[-1]
        if not self.collateral_damage:
            del self.bystander[-1]

    def evaluate_defense(self, score_change='plus'):
        """Check for presence of scoreable operators and grade accordingly."""
        if score_change == 'plus':
                score_change = 1
        else:
                score_change = -1
        # No points at all for ordinary characters; this is not regex.
        # Would fail if ^ or $ at impossible locations, but this situation
        #    never occurs because it is always caught by `re` before the 
        #    present function is called.
        #
        # Two points for character sets with [...], groups with (...), 
        #     and each use of Kleene star * (and +).
        twopoints_charsets = '\[.+?\]'
        self.score += score_change * 2 * len(
                re.findall(twopoints_charsets, self.defense))
        # Delete the contents of [...] so cases of operators .|?^${}() there 
        #     are not counted a second time below.
        self.defense = re.sub(twopoints_charsets, '', self.defense)
        # Score of (...) is different from (?...) so exclude the latter here.
        twopoints_groups_star_plus = '\([^?].*?\)|\*|\+'
        self.score += score_change * 2 * len(
                re.findall(twopoints_groups_star_plus, self.defense))
        #
        # One point for operators ., |, ?, ^, $.
        onepoint = '\.|\||\?|\^|\$'
        self.score += score_change * len(re.findall(onepoint, self.defense))
        #
        # Five points for back-references (\1, etc.) and repetition, 
        #     as {2} or {2, 5}.
        fivepoints_brackets = r'\{\d+,? *\d*?\}'
        self.score += score_change * 5 * len(
                re.findall(fivepoints_brackets, self.defense))
        fivepoints_backref = r'\\\d+'
        self.score += score_change * 5 * len(
                re.findall(fivepoints_backref, self.defense))
        #
        # Ten points for look-ahead and look-behind.
        # Note: ? here already counts as one point so (?...) counts as nine.
        tenpoints = '\(\?.+?\)'
        self.score += score_change * 9 * len(
                re.findall(tenpoints, self.defense))

    def after_defense_is_submitted(self):
        # Check defense against past regexes; invalidate if found.
        if self.defense_submitted in self.defense_record:
            self.message = 'This defense has already been used; invalid.'
            self.invalid_defense = True
            self.attack_successful = False
        # Otherwise, process defense, generate new attack/bystander strings.
        self.new_attacks = True
        self.new_bystander = True
        self.defense_record.add(self.defense_submitted)
        # Evaluate worth of defense.
        self.assess_cycle()
        # Act on attack_successful, collateral_damage
        self.score_defense()
