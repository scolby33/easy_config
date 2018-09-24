# -*- coding: utf-8 -*-

"""Test configuration module for easy_config."""

import os
from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def example_ini(tmpdir_factory) -> Path:
    """Create an example INI configuration file in a temporary directory.

    :returns: the path to the example INI
    """
    example_ini_contents = """[MyProgram]\n# comment\nnumber = 3\nfloaty_number = 5\nflag = False\nword = hello"""
    example_ini_path = tmpdir_factory.mktemp('config').join('example.ini')
    with open(example_ini_path, 'w') as f:
        f.write(example_ini_contents)
    return Path(example_ini_path)


@pytest.fixture(scope='function')
def example_env():
    """Add example values to the environment."""
    os.environ['MYPROGRAM_NUMBER'] = '4'
    os.environ['MYPROGRAM_FLAG'] = 'True'
    yield  # cleanup of new environment variables is necessary
    del os.environ['MYPROGRAM_NUMBER']
    del os.environ['MYPROGRAM_FLAG']


@pytest.fixture(scope='function')
def example_config_env(example_ini):
    """Add example environ config."""
    os.environ['MYPROGRAM_CONFIG'] = str(example_ini)
    yield
    del os.environ['MYPROGRAM_CONFIG']
