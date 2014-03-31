# test_blaster.py
# David Prager Branner
# 20140330

"""Pytest test-suite for the Regex Blaster."""

import blaster as B
import re
import random
import string

looprange = 10

def test_choose_charset_01():
    assert B.choose_charset('a') == string.ascii_lowercase

def test_choose_charset_02():
    assert B.choose_charset() == B.choose_charset('aA')

def test_choose_charset_03():
    assert B.choose_charset('.') == string.punctuation

def test_choose_charset_04():
    assert len(B.choose_charset('a ')) == 39

def test_choose_charset_05():
    assert len(B.choose_charset('aA. ')) == 126

def test_choose_charset_06():
    assert B.choose_charset('0') == '0123456789'

def test_generate_string_01():
    """Test prescribed exact length."""
    for i in range(looprange):
        length = 1 + int(1 / random.random()) * 10
        assert len(B.generate_string(length)) == length 

def test_generate_string_02():
    """Test for presence of space."""
    # Though not certain to be present, is very likely.
    for i in range(looprange):
        assert re.search(' ', B.generate_string(100, 'aA ')).group() == ' '

def test_assess_defense_single_01():
    """Test characters present in empty string."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('.+', B.generate_string(20), '') == (
                True, False)

def test_assess_defense_single_02():
    """Test characters present in both strings."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('.+', B.generate_string(20),
                B.generate_string(20)) == (True, True)

def test_assess_defense_single_03():
    """Test characters present in empty string."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('.+', '', B.generate_string(20)) == (
                False, True)

def test_assess_defense_single_04():
    """Test word with and without letters."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('[a-z ]+', B.generate_string(20, 'a '),
                B.generate_string(20, '.')) == (True, False)

def test_assess_defense_single_05():
    """Test word with and without letters."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('(\w| )+', B.generate_string(20, 'a '),
                B.generate_string(20, '.')) == (True, False)

def test_assess_defense_single_06():
    """Test absence of words in full vs. empty string."""
    s = B.Scorer()
    for i in range(looprange):
        assert s.assess_defense_single('\W*', B.generate_string(20), '') == (
                False, True)

