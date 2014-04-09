## Regex Blaster Past Versions

 * 13 Much `Scorer` material moved into `Scorer` class from `main`. "Noncombatant" changed to "bystander"; all references to time removed from score-line at top of window.

 * 12 Game now ends once either the number of failed defenses or non-combatant deaths reach the maximum, filling the window. The count of the number left is not quite right yet. And the last of the failed defenses or non-combatant deaths does not get reversed.

 * 11 Pruned superfluous class attributes; moved `Timer` and `Scorer` instantiation to main. Changed timing to time passed, with time-limit optional. Revise `evaluate_defense` to both raise and lower score, depending on input, which comes only from `score_defense`. Added 14 working tests for lowering score. Added, then removed, `curses.wrapper()`. Changed `attack` and `noncombatant` to lists (initialized with `[None, None]`; their length is the `y` value in which their last element should be displayed in the appropriate window); when one of them reaches the size of the maximum number of lines, the game ends. Attacks now seem to work correctly, but non-combatants do not.

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
