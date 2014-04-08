## Regex Blaster

**An arcade game to practice regular expressions.**

Currently runs at the command line in both Python 2.6 or 2.7 and Py3 through 3.4. All output is currently via command-line interface.

Outline of game:

 * Computer generates "attack" string; user must supply regex "defense" string to match it. Score is calculated only after return is pressed. 

 * Computer also generates "noncombatant" string; matching these invalidates an otherwise successful defense.

 * Game ends when the "attack" or "noncombatant" window fills with failures.

---

### Scoring

 * No points for ordinary characters (since by themselves they are not yet a regular expression).

 * One point for each operator `.`, `|`, `?`, `^`, `$`.

 * Two points for each character set with `[...]`, each group with `(...)`, and each use of Kleene star `*` (and `+`).

 * Five points for each back-reference (`\1`, etc.) and each case of repetition, as `{2}` or `{2, 5}`.

 * Ten points for each look-ahead and look-behind.

Replacement is not yet dealt with but should also figure.


### To do

To-do list is now a separate file in this directory. (Moved after tag v10.)

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
