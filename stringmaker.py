#! /usr/bin/python
# stringmaker.py
# David Prager Branner
# 20140409

"""Construct interesting strings for Regex Blaster."""

# This file replaces a wholly different `stringmaker.py`, now moved to
# OLD_WORKING/stringmaker_OLD.py.

import string as S
import random as R

# Character inventories:
inventories = {
        'a': S.ascii_lowercase,
        'A': S.ascii_uppercase,
        'n': S.digits,
        }
# Comment: Aim for interesting alternations of substrings made from a few
# distinct characters, in order to draw user's attention to patterns rather
# than cruft.

# Upper bound for any "maximum" values chosen randomly.
upper = 6

def dot():
    """Return any character."""
    # Select inventory at random.
    inventory = R.choice(list(inventories))
    # Select character at random from the inventory.
    return R.choice(inventories[inventory])

def curly_exact(fn, exact):
    """Return an exact number of the outputs of `fn`.

    This is the core function used by all the other repetition functions.
    """
    if not exact:
        return ''
    return ''.join([fn() for i in range(exact)])

##################################################
# Functions below are derivative of `curly_exact`.

def star(fn):
    """Return the repetition, zero or more, of the input."""
    # Equivalent to `curly_min(0)`.
    return curly_min(fn, 0)

def plus(fn):
    # Equivalent to `curly_min(1)`.
    return curly_min(fn, 1)

def curly_min(fn, m):
    """Return random integer, zero or more.

    Note that `n` >= `m`, and that in practice `n` is limited by `upper`.
    """
    n = R.randint(m, upper)
    return curly_range(fn, m, n)

def curly_max(fn, n):
    return curly_range(fn, 0, n)

def curly_range(fn, m, n):
    exact = R.randint(m, n)
    return curly_exact(fn, exact)

##################################################

# Patterns:
patterns = {
        '.': dot(),
        '*': star,
        '+': plus,
        '{n}': curly_exact,
        '{n,}': curly_min,
        '{,n}': curly_max,
        '{m, n}': curly_range
        }

