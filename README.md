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

To-do list is now a separate file `TO-DO.md` in this directory. (Moved after tag v10.)

### Versions

Past versions are now listed in a separate file `VERSIONS.md` in this directory. (Moved after tag v10).

[end]
