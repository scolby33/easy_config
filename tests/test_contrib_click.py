# -*- coding: utf-8 -*-

"""Test the easy_config :mod:`click` wrapper."""

import click
from click.testing import CliRunner

from easy_config import EasyConfig
from easy_config.contrib.click import args_from_config


def test_option():  # noqa: D202
    """Test that when a default is available, a :func:`click.option` is used."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        number: int = 4

    @click.command()
    @args_from_config(ExampleConfig)
    def main(number):
        click.echo(f'number: {number}')

    runner = CliRunner()
    result = runner.invoke(main)
    assert result.output == 'number: 4\n', 'incorrect output'

    result = runner.invoke(main, ['--number', '5'])
    assert result.output == 'number: 5\n'


def test_argument():  # noqa: D202
    """Test that when a default is not available, a :func:`click.argument` is used."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        number: int

    @click.command()
    @args_from_config(ExampleConfig)
    def main(number):
        click.echo(f'number: {number}')

    runner = CliRunner()
    result = runner.invoke(main, ['4'])
    assert result.output == 'number: 4\n'


def test_mixed():  # noqa: D202
    """Test mixed values with/without defaults."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        number: int
        floaty_number: float = 5.0

    @click.command()
    @args_from_config(ExampleConfig)
    def main(number, floaty_number):
        click.echo(f'number: {number}')
        click.echo(f'floaty_number: {floaty_number}')

    runner = CliRunner()
    result = runner.invoke(main, ['4'])
    assert result.output == 'number: 4\nfloaty_number: 5.0\n'
