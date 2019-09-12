import pytest

from grep import ParseError, RegEx


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
    # '[0-9]+[A-Z]*',
])
def test_valid_expressions(expression):
    RegEx(expression)  # should not raise


@pytest.mark.parametrize('expression', [
    '',
    '?', '*', '+',
    '(sdf(sdfds)',
    ']kjlksd',
    # '[3--23]',
    # '[-32]',
    # 'A||B',
    'A()B',
    # 'v(|_)d',
])
def test_invalid_expressions(expression):
    with pytest.raises(ParseError):
        RegEx(expression)


def test_regex():
    regex = RegEx("v(ab)+s")
    import ipdb; ipdb.set_trace()
