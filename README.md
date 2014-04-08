## Regex Blaster

An arcade game to practice regular expressions.

Currently runs at the command line in both Python 2.6 or 2.7 and Py3 through 3.4.

All output is via command-line interface.

Computer generates "attack" string; user must supply regex "defense" string to match it. Score is calculated only after return is pressed.

Computer also generates "noncombatant" string; matching these invalidates an otherwise successful defense.

---

### Scoring

 * No points for ordinary characters (since by themselves they are not yet a regular expression).

 * One point for each operator `.`, `|`, `?`, `^`, `$`.

 * Two points for each character set with `[...]`, each group with `(...)`, and each use of Kleene star `*` (and `+`).

 * Five points for each back-reference (`\1`, etc.) and each case of repetition, as `{2}` or `{2, 5}`.

 * Ten points for each look-ahead and look-behind.

Replacement is not yet dealt with but should also figure.


### To do

 1. Better name for `damage`; implement it and `level`.

 1. Add option for logging.

 1. Add option for pre-defined series of levels.

 1. Handle failed attack and non-combatant strings without inadvertently pausing program.

 1. Need more productive attacks and noncombatants

 1. Abstract `Timer` and `Scorer` from `CursesDisplay`.

 1. Use `argparse` for some command-line options: `random.seed()` for `--debug`.

 1. Apply regex to attack string and non-combatant strings, showing partial matches in real time.

 1. Multiple attack and/or noncombatant strings. More points for multiple matches at once.

 1. ESC: toggle pause/continue; from paused state, h => help page.

 1. Handle arrow keys. Related to handling of ESC; see http://stackoverflow.com/a/1182680/621762.

 1. Report results in file or to screen on close.

 1. Help page on start-up. 
 
 1. User corrects regex offered by machine.

 1. Set background color: automatically black for now.

 1. Handle near-identical defenses:

  2. evaluate by edit-distance vis-à-vis all previous defenses; average string-length minus edit-distance may be more useful than edit-distance alone.
  2. **DONE**: handle by repeating attack string; repeat defense barred;
  2. handle by delaying efficacy, thus increasing risk of hit (San's  suggestion); this requires implementing timing.

 1. Generate progressively more complex attack strings. There are presumably ways to do this formulaically. We should also try to create noncombatant strings and attack strings in such a way as to be difficult to distinguish.

 1. Invalid defense string may lead to score reduction or other penalties.

 1. Program generates regex and user must supply matching string.

 1. Evaluate quality of defense for more scores or greater level increase.

 1. Figure damage (from hits); it may affect time of defense's effect..

 1. For more complex attacks, it may be interesting to repeat them just in order to see how many different defenses the user can supply. Keep repeating until user fails — or even a little after that.

 1. If \w appears a lot, add whitespace.

 1. JS version.

### Versions

 * 10 Changes to `evaluate_defense` and 14 working tests.

 * 09 `evaluate_defense` appears to be working for scoring (lookaround not yet checked); test suite created for this.

 * 08 Changed name of main file to to `regex_blaster`; `Timer`, `Scorer`, and `CursesDisplay` moved out to discrete files. `CursesDisplay.fade_out` and `CursesDisplay.highlight_failure` work. Problems: 

   * if defense is a repeat, user needs to be able to try again (**DONE** in 09);
   * don't generate new noncombatant if existing non-combatant is not martyred (**DONE** in 09);
   * if defense succeeds, next attack is in same place as previous one;
   * need more productive attacks and noncombatants;
   * better name for "damage";
   * need scoring program to evaluate defense strings.

 * 07 Unique failed defense string generates new attack and noncombatant strings.

 * 06 Control window size. Move message to `rjust()`. Move `defense` and `message` strings to `Scorer`. Goal: to segregate all Curses-related functionality in `Window` class, so that JS version can be added withough substantial refactoring.

 * 05 Color and label different sub-windows. Trap delete and CR control chars.

 * 04 Set up different sub-windows. Separate Timer class. Defense line.

 * 03 Get styled text working; no display delay on startup..

 * 02 Set up and close curses in special functions; always trap ctrl-c.

 * 01 Open window; close on two backticks.


[end]
