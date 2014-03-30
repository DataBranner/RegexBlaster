# test_blaster.py
# David Prager Branner
# 20140330

"""Pytest test-suite for the Regex Blaster."""

import blaster as B
import re
import random
import string

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

def test_assess_defense_single_01():
    pass

