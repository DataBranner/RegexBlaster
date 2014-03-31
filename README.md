## Regex Blaster

An arcade game to practice regular expressions.

---

### To do

 1. Show partial matches in real time.
 
 1. Multiple attack and/or noncombatant strings. More points for multiple matches at once.

 1. User corrects regex offered by machine.

 1. Handle near-identical defenses:

  2. evaluate by edit-distance vis-à-vis all previous defenses; average  string-length minus edit-distance may be more useful than edit-distance alone.
  2. handle by repeating attack string; repeat defense barred;
  2. handle by delaying efficacy, thus increasing risk of hit (San's  suggestion); this requires implementing timing.

 1. Generate progressively more complex attack strings. There are presumably ways to do this formulaically. We should also try to create noncombatant strings and attack strings in such a way as to be difficult to distinguish.

 1. Invalid defense string may lead to score reduction or other penalties.

 1. Evaluate quality of defense for more scores or greater level increase.

 1. Figure damage (from hits); it may affect time of defense's effect..

 1. For more complex attacks, it may be interesting to repeat them just in order to see how many different defenses the user can supply. Keep repeating until user fails — or even a little after that.

 1. If \w appears a lot, add whitespace.

[end]
