## Regex Blaster To-do List

 1. Need more productive attacks and noncombatants; revise `stringmaker.py` and incorporate into main program: 

  2. levels, allowing progressively more complex attack strings
  2. generate attack/noncombatant strings formulaically
  2. noncombatant strings and attack strings should be related in such a way as to be difficult to distinguish.

 1. Use `argparse` for some command-line options: 

  2. `--debug`: turns on `random.seed()`; 
  2. `--log` (must first implement logging); 
  2. `--help`: show rules without running program?;
  2. `--levels`: pre-defined series of levels, for systematic practice.

 1. Change list of failed attacks to dict, to enable counting. Bring both failed and defeated attacks back repeatedly.

 1. Handle failed attack and non-combatant strings without inadvertently pausing program.

 1. Apply regex to attack string and non-combatant strings, showing partial matches in real time.

 1. ESC: toggle pause/continue; from paused state, h => help page.

 1. Handle arrow keys. Related to handling of ESC; see http://stackoverflow.com/a/1182680/621762.

 1. Help page on start-up. 
 
 1. Alternate game strategies:

  2. User corrects regex offered by machine.
  2. Multiple attack and/or noncombatant strings. More points for multiple matches at once.

 1. Handle near-identical defenses:

  2. evaluate by edit-distance vis-à-vis all previous defenses; average string-length minus edit-distance may be more useful than edit-distance alone.
  2. **DONE**: handle by repeating attack string; repeat defense barred;
  2. handle by delaying efficacy, thus increasing risk of hit; this requires implementing timing of attacks (not sure if this is desirable until higher levels).

 1. Figure damage (from hits); it may affect time of defense's effect.

 1. For more complex attacks, it may be interesting to repeat them just in order to see how many different defenses the user can supply. Keep repeating until user fails — or even a little after that.

 1. If \w appears a lot in defense strings, add whitespace.

 1. Set background color: automatically black for now.

 1. JS version.

[end]
