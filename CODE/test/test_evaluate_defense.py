import scorer

def test_evaluate_defense_01():
    """Test wildcards."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.g.'
    S.evaluate_defense()
    assert S.score == 3

def test_evaluate_defense_02():
    """Test wildcards and end-string."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.g.$'
    S.evaluate_defense()
    assert S.score == 4

def test_evaluate_defense_03():
    """Test wildcards and start-string."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '^.t.g.'
    S.evaluate_defense()
    assert S.score == 4

def test_evaluate_defense_04():
    """Test wildcards and one group"""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t.g.'
    S.evaluate_defense()
    assert S.score == 5

def test_evaluate_defense_05():
    """Test wildcards and two groups."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.)g.'
    S.evaluate_defense()
    assert S.score == 7

def test_evaluate_defense_06():
    """Test OR, groups, wildcard."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.|x)g.'
    S.evaluate_defense()
    assert S.score == 8

def test_evaluate_defense_07():
    """Test OR, groups, wildcard, Kleene star."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.|x)gH*.'
    S.evaluate_defense()
    assert S.score == 10

def test_evaluate_defense_08():
    """Test three wildcards and three curly brackets."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.{1}g{1}H{0}.'
    S.evaluate_defense()
    assert S.score == 18

def test_evaluate_defense_09():
    """Test wildcards, group, one backref."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = r'(.)t\1g.'
    S.evaluate_defense()
    assert S.score == 9

def test_evaluate_defense_10():
    """Test wildcards, group, one backref, one repetition."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'(.)t\1{2}g.'
    S.evaluate_defense()
    assert S.score == 14

def test_evaluate_defense_11():
    """Test wildcards, group, backref, repetition, negative lookahead."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'(.)t\1{2}g.(?!X)'
    S.evaluate_defense()
    assert S.score == 24

def test_evaluate_defense_12():
    """Test wildcards, group, backref, repetition, lookarounds.."""
    S = scorer.Scorer()
    S.attack = '7ataac'
    S.defense = r'(?=7)(.)t\1{2}g.(?!X)'
    S.evaluate_defense()
    assert S.score == 34

def test_evaluate_defense_13():
    """Test wildcards, charset."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = '.t..[a2;].'
    S.evaluate_defense()
    assert S.score == 6

def test_evaluate_defense_14():
    """Test wildcards, and positive/negative charsets."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'.[^F]..[a2;].'
    S.evaluate_defense()
    assert S.score == 8


def test_evaluate_defense_15():
    """Test wildcards."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.g.'
    S.evaluate_defense('minus')
    assert S.score == -3

def test_evaluate_defense_16():
    """Test wildcards and end-string."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.g.$'
    S.evaluate_defense('minus')
    assert S.score == -4

def test_evaluate_defense_17():
    """Test wildcards and start-string."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '^.t.g.'
    S.evaluate_defense('minus')
    assert S.score == -4

def test_evaluate_defense_18():
    """Test wildcards and one group"""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t.g.'
    S.evaluate_defense('minus')
    assert S.score == -5

def test_evaluate_defense_19():
    """Test wildcards and two groups."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.)g.'
    S.evaluate_defense('minus')
    assert S.score == -7

def test_evaluate_defense_20():
    """Test OR, groups, wildcard."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.|x)g.'
    S.evaluate_defense('minus')
    assert S.score == -8

def test_evaluate_defense_21():
    """Test OR, groups, wildcard, Kleene star."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = '(.)t(.|x)gH*.'
    S.evaluate_defense('minus')
    assert S.score == -10

def test_evaluate_defense_22():
    """Test three wildcards and three curly brackets."""
    S = scorer.Scorer()
    S.attack = 'atbgc'
    S.defense = '.t.{1}g{1}H{0}.'
    S.evaluate_defense('minus')
    assert S.score == -18

def test_evaluate_defense_23():
    """Test wildcards, group, one backref."""
    S = scorer.Scorer()
    S.attack = 'atagc'
    S.defense = r'(.)t\1g.'
    S.evaluate_defense('minus')
    assert S.score == -9

def test_evaluate_defense_24():
    """Test wildcards, group, one backref, one repetition."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'(.)t\1{2}g.'
    S.evaluate_defense('minus')
    assert S.score == -14

def test_evaluate_defense_25():
    """Test wildcards, group, backref, repetition, negative lookahead."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'(.)t\1{2}g.(?!X)'
    S.evaluate_defense('minus')
    assert S.score == -24

def test_evaluate_defense_26():
    """Test wildcards, group, backref, repetition, lookarounds.."""
    S = scorer.Scorer()
    S.attack = '7ataac'
    S.defense = r'(?=7)(.)t\1{2}g.(?!X)'
    S.evaluate_defense('minus')
    assert S.score == -34

def test_evaluate_defense_27():
    """Test wildcards, charset."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = '.t..[a2;].'
    S.evaluate_defense('minus')
    assert S.score == -6

def test_evaluate_defense_28():
    """Test wildcards, and positive/negative charsets."""
    S = scorer.Scorer()
    S.attack = 'ataac'
    S.defense = r'.[^F]..[a2;].'
    S.evaluate_defense('minus')
    assert S.score == -8


