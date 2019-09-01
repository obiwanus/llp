import pytest

from grep import is_valid, grep


@pytest.mark.parametrize('expression', [
    'a',
    'AaaAa ',
    '^sdfn a$',
    'asd(vasia)f(petya)',
    '(sjdf)|(nri2n)',
    'Ihjhs*hjs*',
    'skd+sdln+',
    'nsdn(sdf)?',
    '.+-(32)+',
    '[0-9]+[A-Z]*',
])
def test_valid_expressions(expression):
    assert is_valid(expression)


@pytest.mark.parametrize('expression', [
    '',
    '?', '*', '+',
    '(sdf(sdfds)',
    ']kjlksd',
    '[323]',
    '[1-32]',
    'A||B',
    'A()B',
    'v(|_)d',
])
def test_invalid_expressions(expression):
    assert is_valid(expression) is False
