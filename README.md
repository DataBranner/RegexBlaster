## Regex Blaster

**An arcade game to practice regular expressions.**

Currently runs at the command line in both Python 2.6 or 2.7 and Py3 through 3.4. All output is currently via command-line interface. This is a proof of concept; more features are in the pipeline, but the code runs and the game plays right now.

Run at the command line:

    python regex_regex_blaster_14.py

and the contents of the terminal window will be replaced with the game window.

To quit at any time, hit the ESC (escape) key.

**Outline of game**:

 * Computer generates "attack" string; user must supply regex "defense" string to match it. Score is calculated only after return is pressed. If the defense string is invalid or fails to match the attack, the attack is successful and the user is a step closer to losing the game.

 * Computer also generates "bystander" strings, which you must not "kill" with your defense string. Matching a bystander string invalidates an otherwise successful defense and also brings the user closer to losing the game.

 * Game ends when either the "attack" or "noncombatant" window fills with failures. By design there is no time pressure in this game.

**Gameplay examples**:

 [Coming soon.]

---

### Scoring

 * No points for ordinary characters (since by themselves they are not yet a regular expression).

 * One point for each operator `.`, `|`, `?`, `^`, `$`.

 * Two points for each character set with `[...]`, each group with `(...)`, and each use of Kleene star `*` (and `+`).

 * Five points for each back-reference (`\1`, etc.) and each case of repetition, as `{2}` or `{2, 5}`.

 * Ten points for each look-ahead and look-behind.

Replacement is not yet dealt with but should also figure.

### Background

People who feel weak at regular expressions can improve if they practice. This game is intended to help them do just that.

I had originally planned a Space Invaders-type shoot'em-up game using JavaScript, in which you are attacked by strings and have to defend yourself with regex. In order to work up a proof-of-concept using the Python backend, I turned to the Curses library, and the resulting command-line interface seems to me effective.

Early in the implementation, I found that the two most characteristic aspects of the shoot'em-up plan — racing the clock and moving targets — did not improve the learning aspect of the game. A good regular expression may take a little time to compose, and moving text is needlessly difficult to focus on. So I've moved instead to a model in which the user wins points by coming up with multiple and diverse "defense" strings, and time is not counted.

### State of development

The game presently (20140410) works but a good deal of further functionality has still to be implemented. What you have here is a proof of concept.

### Contents of this directory

 * main file: `regex_blaster_14.py` (or subsequently numbered versions)
 * supporting classes:

   * `cursesdisplay.py`
   * `scorer.py`
   * `timer.py`
   * `stringmaker.py`

 * `pytest` test suite: `test/`
 * directories containing files for my reference:

   * `OLD_WORKING`
   * `REFERENCE`

 * this README and supporting development information:

   * `VERSIONS.md`
   * `TO-DO..md`

### To do

To-do list is now a separate file `TO-DO.md` in this directory. (Moved after tag v10.)

### Versions

Past versions are now listed in a separate file `VERSIONS.md` in this directory. (Moved after tag v10).

[end]
