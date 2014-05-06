#! /usr/bin/python
# stringmaker.py
# David Prager Branner
# 20140410

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
upper_limit = 6

def dot(inventory=None):
    """Return any character."""
    if not inventory or inventory not in inventories:
        # Select inventory at random if a viable one is not provided.
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

def charset(char_list):
    """Return a single character selected from char_list."""
    # Negation with `^`.
    if char_list[0] == '^':
        while True:
            char = dot()
            if char not in char_list:
                return char
    return R.choice(list(set(char_list)))

def make_word(length=upper_limit, inventory=None):
    """Generate a 'word' of given length."""
    return ''.join([dot(inventory) for i in range(length)])

def make_run(length=upper_limit, inventory=None):
    """Generate a consecutive run of a single character."""
    char = dot(inventory)
    return ''.join([char for i in range(length)])

def make_long_string(
        words=upper_limit//2, inventory=None, dups=True, delim=' '):
    """Generate a series of space-delimited 'words'."""
    kind = [make_word, make_run]
    words_made = [R.choice(kind)(inventory=inventory) for i in range(words)]
    if dups:
        return delim.join([R.choice(words_made) for i in range(words)])
    else:
        return delim.join(words_made)

combinations = []

##################################################
# Functions below are derivatives of others.

def digit():
    """Return a single digit, equivalent to \d."""
    return dot('n')

def star(fn):
    """Return the repetition, zero or more, of the input."""
    # Equivalent to `curly_min(0)`.
    return curly_min(fn, 0)

def plus(fn):
    """Return the repetition, one or more, of the input."""
    # Equivalent to `curly_min(1)`.
    return curly_min(fn, 1)

def curly_min(fn, m):
    """Return random number of examples of fn, no fewer than `m`."""

    n = R.randint(m, upper_limit)
    return curly_range(fn, m, n)

def curly_max(fn, n):
    """Return random number of examples of fn, no more than `n`."""
    return curly_range(fn, 0, n)

def curly_range(fn, m, n):
    """Return random number of examples of fn, minimum `m`, maximum `n`.

    Note that `n` >= `m`, and that in practice `n` is limited by `upper_limit`.
    """
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
        '{m, n}': curly_range,
        '[...]': charset,
        }

