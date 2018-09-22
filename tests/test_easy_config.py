"""Tests for the EasyConfig class."""
from io import StringIO

import pytest

from easy_config import EasyConfig


class ExampleConfig(EasyConfig):
    FILES = None
    NAME = 'MyProgram'

    number: int
    floaty_number: float
    flag: bool
    word: str


def test_unsubclassed_easy_config_raises():
    with pytest.raises(NotImplementedError):
        EasyConfig()


def test_load_file(example_ini):
    result = {
        'number': 3,
        'floaty_number': 5.0,
        'flag': False,
        'word': 'hello',
    }
    assert ExampleConfig._load_file(example_ini) == result
    assert ExampleConfig._load_file(str(example_ini)) == result
    with open(example_ini, 'r') as f:
        assert ExampleConfig._load_file(f) == result

    empty_file = StringIO()
    assert ExampleConfig._load_file(empty_file) == {}

    empty_section = StringIO('[MyProgram]')
    assert ExampleConfig._load_file(empty_section) == {}


def test_load_environment(example_env):
    assert ExampleConfig._load_environment() == {'number': 4, 'flag': True}


def test_load_dict():
    assert ExampleConfig._load_dict({'number': '3', 'unused': 'foo'}) == {'number': 3}


def test_load(example_ini, example_env):
    a = ExampleConfig.load([example_ini], parse_environment=False)
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'

    b = ExampleConfig.load([example_ini])
    assert b.number == 4
    assert b.floaty_number == 5.0
    assert b.flag is True
    assert b.word == 'hello'

    c = ExampleConfig.load([example_ini], parse_environment=False, number=10)
    assert c.number == 10
    assert c.floaty_number == 5.0
    assert c.flag is False
    assert c.word == 'hello'

    d = ExampleConfig.load(floaty_number=9, word='world')
    assert d.number == 4
    assert d.floaty_number == 9.0
    assert d.flag is True
    assert d.word == 'world'

    with pytest.raises(TypeError) as excinfo:
        e = ExampleConfig.load(parse_environment=False)
    assert str(excinfo.value) == 'missing some configuration values'
