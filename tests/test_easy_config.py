# -*- coding: utf-8 -*-

"""Tests for the EasyConfig class."""

import os
from io import StringIO

import pytest

from easy_config import EasyConfig


class ExampleConfig(EasyConfig):
    """Example EasyConfig subclass to test with."""

    FILES = None
    NAME = 'MyProgram'

    number: int
    floaty_number: float
    flag: bool
    word: str


def test_unsubclassed_easy_config_raises():
    """Test that a plain EasyConfig can't be instantiated."""
    with pytest.raises(TypeError) as excinfo:
        EasyConfig()
    assert str(excinfo.value) == 'EasyConfig must be subclassed'


def test_read_file(example_ini):
    """Test EasyConfig._read_file functionality with all permutations of input types."""
    result = {'number': 3, 'floaty_number': 5.0, 'flag': False, 'word': 'hello'}
    assert ExampleConfig._read_file(example_ini) == result
    assert ExampleConfig._read_file(str(example_ini)) == result
    with open(example_ini, 'r') as f:
        assert ExampleConfig._read_file(f) == result

    empty_file = StringIO()
    assert ExampleConfig._read_file(empty_file) == {}

    empty_section = StringIO('[MyProgram]')
    assert ExampleConfig._read_file(empty_section) == {}


def test_read_environment(example_env):
    """Test EasyConfig._read_environment."""
    assert ExampleConfig._read_environment() == {'number': 4, 'flag': True}


def test_load_from_env(example_config_env):
    """Test EasyConfig.load with _lookup_config_envvar."""
    assert (
        'MYPROGRAM_FLAG' not in os.environ
    ), 'This environment variable should have been cleaned up by pytest'
    assert (
        'MYPROGRAM_NUMBER' not in os.environ
    ), 'This environment variable should have been cleaned up by pytest'

    a = ExampleConfig.load(parse_files=False, _lookup_config_envvar='config')
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'


def test_load_from_env_unset():
    """Test looking up a config file via an environment variable that isn't set."""
    a = ExampleConfig.load(
        number=3,
        floaty_number=5,
        flag=False,
        word='hello',
        _lookup_config_envvar='config',
    )
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'


def test_load_from_env_empty(example_config_env_empty):
    """Test looking up a config file via an environment variable that is set to an empty string."""
    a = ExampleConfig.load(
        number=3,
        floaty_number=5,
        flag=False,
        word='hello',
        _lookup_config_envvar='config',
    )
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'


def test_load_from_env_missing(example_config_env_missing):
    """Test looking up a config file via an environment variable that is set to a nonexistent file."""
    a = ExampleConfig.load(
        number=3,
        floaty_number=5,
        flag=False,
        word='hello',
        _lookup_config_envvar='config',
    )
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'


def test_read_dict():
    """Test EasyConfig._read_dict."""
    assert ExampleConfig._read_dict({'number': '3', 'unused': 'foo'}) == {'number': 3}


def test_load(example_ini, example_env):
    """Test EasyConfig.load."""
    a = ExampleConfig.load([example_ini], _parse_environment=False)
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'

    b = ExampleConfig.load([example_ini])
    assert b.number == 4
    assert b.floaty_number == 5.0
    assert b.flag is True
    assert b.word == 'hello'

    c = ExampleConfig.load([example_ini], _parse_environment=False, number=10)
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
        ExampleConfig.load(_parse_environment=False)
    assert str(excinfo.value) == 'missing some configuration values'


def test_load_with_default_files(example_ini):
    """Test EasyConfig.load when the class FILES variable is populated."""
    class ExampleWithFiles(ExampleConfig):
        FILES = [example_ini]

    a = ExampleWithFiles.load(_parse_environment=False)
    assert a.number == 3
    assert a.floaty_number == 5.0
    assert a.flag is False
    assert a.word == 'hello'


def test_load_raises_plain_type_error():
    """Test that EasyConfig.load properly re-raises a TypeError not related to the number of arguments."""
    class ExampleWithTypeErrorInit(ExampleConfig):
        def __init__(self, *_args, **_kwargs):
            raise TypeError('testing type error')

    with pytest.raises(TypeError) as excinfo:
        ExampleWithTypeErrorInit.load()
    assert str(excinfo.value) == 'testing type error'


def test_dump():
    """Test EasyConfig.dump to a file."""
    a = ExampleConfig.load(number=3, floaty_number=5.0, flag=False, word='hello')
    output = StringIO()
    a.dump(output)
    output_lines = output.getvalue().splitlines(keepends=True)
    assert output_lines[0] == '[MyProgram]\n'
    assert 'number = 3\n' in output_lines
    assert 'floaty_number = 5.0\n' in output_lines
    assert 'flag = False\n' in output_lines
    assert 'word = hello\n' in output_lines
