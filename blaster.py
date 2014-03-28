#!/usr/bin/python3
# blaster.py
# David Prager Branner

"""Game to improve regex skills."""

# For later:
#  1. Handle near-identical entries.
#   a. evaluate by edit-distance
#   a. handle by repeating attack string; repeat defense barred.
#   b. handle by delaying efficacy, thus increasing risk of hit (San's
#      suggestion); this requires implementing timing.
#  2. Generate progressively more complex attack strings. There are presumably
#     ways to do this formulaic.

def main():
    alive = True
    # set up variables
    score = 0
    defnse_record = set()
    while alive:
        # generate "attack" string (must be matched to avoid hit)
        # generate "rescue" string (must be matched to avoid point-loss)
        # collect "defense" (user regex)
        # check defense against past regexes; invalidate if found
        # test defense against "attack" and figure point change
        # test defense against "rescue" and figure point change
        pass
