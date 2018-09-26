# -*- coding: utf-8 -*-

"""A wrapper for generating options for a :mod:`click` command from an :class:`easy_config.EasyConfig`."""

import dataclasses
from typing import Callable, Type

import click

from easy_config import EasyConfig

__all__ = [
    'args_from_config',
]

# A callable that can take in anything, but gives back nothing
GenericCallable = Callable[..., None]


def args_from_config(cls: Type[EasyConfig]) -> Callable[[GenericCallable], GenericCallable]:  # noqa: D202
    """Build a decorator based on the given easy config class."""

    def decorate(command: GenericCallable) -> GenericCallable:
        """Decorate the :mod:`click` command."""
        for field in dataclasses.fields(cls):
            if field.default is dataclasses.MISSING:
                wrapper = click.argument(field.name, type=field.type)
            else:
                wrapper = click.option(f'--{field.name}', type=field.type, default=field.default)

            command = wrapper(command)

        return command

    return decorate
