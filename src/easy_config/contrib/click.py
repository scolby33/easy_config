# -*- coding: utf-8 -*-

"""Test the click wrapper."""

import dataclasses
from typing import Callable, Type

import click

from easy_config import EasyConfig


def args_from_config(cls: Type[EasyConfig]) -> Callable[[Callable], Callable]:  # noqa: D202
    """Build a decorator based on the given easy config class."""

    def decorate(command: Callable) -> Callable:
        """Decorate the :mod:`click` command."""
        for field in dataclasses.fields(cls):
            if field.default is dataclasses.MISSING:
                wrapper = click.argument(field.name, type=field.type)
            else:
                wrapper = click.option(f'--{field.name}', type=field.type, default=field.default)

            command = wrapper(command)

        return command

    return decorate
