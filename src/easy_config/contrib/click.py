# -*- coding: utf-8 -*-

"""A wrapper for generating options for a :mod:`click` command from an :class:`easy_config.EasyConfig`."""

import dataclasses
from typing import Any, Callable, Type, TypeVar

import click

from easy_config import EasyConfig

__all__ = [
    'args_from_config',
    'config_command',
]

# declaring types for the decorator
# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)

Func2Type = Callable[[EasyConfig], Any]
G = TypeVar('G', bound=Func2Type)


def args_from_config(cls: Type[EasyConfig]) -> Callable[[F], F]:  # noqa: D202
    """Build a decorator based on the given easy config class."""

    def decorate(command: F) -> F:
        """Decorate the :mod:`click` command."""
        for field in dataclasses.fields(cls):
            if field.default is dataclasses.MISSING:
                wrapper = click.argument(field.name, type=field.type)
            else:
                wrapper = click.option(
                    f'--{field.name}', type=field.type, default=field.default, show_default=True
                )

            command = wrapper(command)

        return command

    return decorate


def config_command(cls: Type[EasyConfig]) -> Callable[[G], F]:  # noqa: D202
    """Build a decorator based on the given easy config class.

    This makes it possible to automatically generate the :py:func:`click.argument` and :py:func:`click.option` entries
    for a command for a given :py:class:`EasyConfig` class. For example, if you have a python file called ``main.py``:

    .. code-block:: python

        import click
        from easy_config import EasyConfig
        from easy_config.contrib.click import config_command

        class ExampleConfig(EasyConfig):
            FILES = None
            NAME = 'MyProgram'

            number: int
            floaty_number: float = 5.0

        @click.command()
        @config_command(ExampleConfig)
        def main(example_config: ExampleConfig):
            click.echo(f'number: {example_config.number}')
            click.echo(f'floaty_number: {example_config.floaty_number}')

        if __name__ == '__main__':
            main()

    And run it with ``python main.py``, you will get:

    .. code-block:: sh

        Usage: scratch.py [OPTIONS] NUMBER

          Apply the keyword arguments to the EasyConfig class.

        Options:
          --floaty_number FLOAT
          --help                 Show this message and exit.
    """

    def decorate(command: G) -> F:  # noqa: D202
        """Decorate the :mod:`click` command."""

        @args_from_config(cls)
        def inner_decorate(**kwargs: Any) -> Any:
            """Apply the keyword arguments to the EasyConfig class."""
            return command(cls.load(**kwargs))

        return inner_decorate  # type: ignore

    return decorate
