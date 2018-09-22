"""Tests for the EasyConfig class."""

from easy_config import EasyConfig

class A(EasyConfig):
    FILES = ['myprogram.ini']
    NAME = 'MyProgram'

    number: int
    name: str
    check_bounds: bool = True


def test_load_file(example_ini):
    class TestConfig(EasyConfig):
        FILES = None
        NAME = 'MyProgram'

        number: int

    assert TestConfig._load_file(example_ini) == {'number': 3}
    assert TestConfig._load_file(str(example_ini)) == {'number': 3}
    with open(example_ini, 'r') as f:
        assert TestConfig._load_file(f) == {'number': 3}
