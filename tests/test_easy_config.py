"""Tests for the EasyConfig class."""

from easy_config import EasyConfig


class ExampleConfig(EasyConfig):
    FILES = None
    NAME = 'MyProgram'

    number: int
    floaty_number: float
    flag: bool
    word: str



def test_load_file(example_ini):
    assert ExampleConfig._load_file(example_ini) == {'number': 3}
    assert ExampleConfig._load_file(str(example_ini)) == {'number': 3}
    with open(example_ini, 'r') as f:
        assert ExampleConfig._load_file(f) == {'number': 3}


def test_load_environment(example_env):
    assert ExampleConfig._load_environment() == {'number': 3}


def test_load_dict():
    assert ExampleConfig._load_dict({'number': '3', 'unused': 'foo'}) == {'number': 3}
