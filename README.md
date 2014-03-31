## Regex Blaster

An arcade game to practice regular expressions.

---

### For later

 1. Handle near-identical defenses:

  a. evaluate by edit-distance vis-à-vis all previous defenses; average  string-length minus edit-distance may be more useful than edit-distance alone.
  b. handle by repeating attack string; repeat defense barred;
  c. handle by delaying efficacy, thus increasing risk of hit (San's  suggestion); this requires implementing timing.

 2. Generate progressively more complex attack strings. There are presumably ways to do this formulaically. We should also try to create noncombatant strings and attack strings in such a way as to be difficult to distinguish.

 3. In future we may want multiple attack and/or noncombatant strings.

 4. Invalid defense string may lead to score reduction or other penalties.

 5. Evaluate quality of defense for more scores or greater level increase.

 6. Figure damage (from hits); it may affect time of defense's effect..

 7. For more complex attacks, it may be interesting to repeat them just in order to see how many different defenses the user can supply. Keep repeating until user fails — or even a little after that.

 8. If \w appears a lot, add whitespace.

[end]