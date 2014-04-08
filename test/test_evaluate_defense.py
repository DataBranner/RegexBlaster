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
    assert S.score == 8

def test_evaluate_defense_07():
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


