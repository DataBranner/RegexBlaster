# test_stringmaker.py
# David Prager Branner
# 20140410

import stringmaker as M
import random as R
import time as T

range_value = 100

def test_dot_01():
    """Test length of dot() output."""
    for i in range(range_value):
        assert len(M.dot()) == 1

def test_dot_02():
    """Test use of inventory 'a' with dot()."""
    for i in range(range_value):
        assert M.dot('a') in M.inventories['a']

def test_dot_03():
    """Test use of inventory 'A' with dot()."""
    for i in range(range_value):
        assert M.dot('A') in M.inventories['A']

def test_dot_04():
    """Test use of inventory 'n' with dot()."""
    for i in range(range_value):
        assert M.dot('n') in M.inventories['n']

def test_dot_05():
    """Test use of randomly chosen inventory with dot()."""
    for i in range(range_value):
        inventory = R.choice(list(M.inventories))
        assert M.dot(inventory) in M.inventories[inventory]

def test_star_01():
    """Test that plus() == curly_min(0)"""
    for i in range(range_value):
        seed = T.time()
        R.seed(seed)
        star = M.star(M.dot)
        R.seed(seed)
        assert star == M.curly_min(M.dot, 0)

def test_plus_01():
    """Test that plus() == curly_min(1)"""
    for i in range(range_value):
        seed = T.time()
        R.seed(seed)
        star = M.plus(M.dot)
        R.seed(seed)
        assert star == M.curly_min(M.dot, 1)

def test_charset_01():
    """Test use of charset with list."""
    for i in range(range_value):
        inventory = R.choice(list(M.inventories))
        char_list = [R.choice(list(M.inventories[inventory])) 
                for i in range(range_value)]
        assert M.charset(char_list) in M.inventories[inventory]

def test_charset_02():
    """Test use of charset with string."""
    for i in range(range_value):
        inventory = R.choice(list(M.inventories))
        char_list = ''.join([R.choice(list(M.inventories[inventory])) 
                for i in range(range_value)])
        assert M.charset(char_list) in M.inventories[inventory]

def test_charset_03():
    """Test use of negative charset with list."""
    for i in range(range_value):
        inventory = R.choice(list(M.inventories))
        char_list = ['^'] + [R.choice(list(M.inventories[inventory])) 
                for i in range(range_value)]
        char = M.charset(char_list)
        assert char not in char_list

def test_charset_04():
    """Test use of negative charset with string."""
    for i in range(range_value):
        inventory = R.choice(list(M.inventories))
        char_list = '^' + ''.join([R.choice(list(M.inventories[inventory])) 
                for i in range(range_value)])
        assert M.charset(char_list) not in char_list

