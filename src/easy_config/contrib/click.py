# -*- coding: utf-8 -*-

"""A wrapper for generating options for a :mod:`click` command from an :class:`easy_config.EasyConfig`."""

import dataclasses
from typing import Any, Callable, Type, TypeVar

import click

from easy_config import EasyConfig

__all__ = [
    'args_from_config',
]

# declaring types for the decorator
# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)


def args_from_config(cls: Type[EasyConfig]) -> Callable[[F], F]:  # noqa: D202
    """Build a decorator based on the given easy config class."""

    def decorate(command: F) -> F:
        """Decorate the :mod:`click` command."""
        for field in dataclasses.fields(cls):
            if field.default is dataclasses.MISSING:
                wrapper = click.argument(field.name, type=field.type)
            else:
                wrapper = click.option(f'--{field.name}', type=field.type, default=field.default, show_default=True)

            command = wrapper(command)

        return command

    return decorate
