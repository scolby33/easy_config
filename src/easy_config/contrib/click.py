# -*- coding: utf-8 -*-

"""A wrapper for generating options for a :mod:`click` command from an :class:`easy_config.EasyConfig`."""

import dataclasses
from typing import Any, Callable, Type, TypeVar

import click

from easy_config import EasyConfig

__all__ = [
    'args_from_config',
    'easy_config_option',
]

# declaring types for the decorator
# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)

Func2Type = Callable[[EasyConfig], Any]
G = TypeVar('G', bound=Func2Type)


def easy_config_option(cls: Type[EasyConfig], prompt: bool = False) -> Callable[[G], F]:  # noqa: D202
    """Build a decorator based on the given easy config class.

    :param cls: An EasyConfig class
    :param prompt: If true, adds prompts to the resulting CLI for all fields.

    This makes it possible to automatically generate the :py:func:`click.argument` and :py:func:`click.option` entries
    for a command for a given :py:class:`easy_config.EasyConfig` class. For example, if you have a python file called
    ``main.py``:

    .. code-block:: python

        # main.py

        import click
        from easy_config import EasyConfig
        from easy_config.contrib.click import easy_config_option

        class ExampleConfig(EasyConfig):
            FILES = None
            NAME = 'MyProgram'

            number: int
            floaty_number: float = 5.0

        @click.command()
        @easy_config_option(ExampleConfig)
        def main(example_config: ExampleConfig):
            click.echo()
            click.echo('RESULTS')
            click.echo(f'number: {example_config.number}')
            click.echo(f'floaty_number: {example_config.floaty_number}')

        if __name__ == '__main__':
            main()

    And run it with ``python main.py``, you will get:

    .. code-block:: sh

        Usage: main.py [OPTIONS] NUMBER

          Apply the keyword arguments to the EasyConfig class.

        Options:
          --floaty_number FLOAT  [default: 5.0]
          --help                 Show this message and exit.

    Modifying the code slightly to use ``@easy_config_option(ExampleConfig, prompt=True)`` will give the following CLI:

    .. code-block:: sh

        Usage: main.py [OPTIONS]

          Apply the keyword arguments to the EasyConfig class.

        Options:
          --floaty_number FLOAT  [default: 5.0]
          --number INTEGER
          --help                 Show this message and exit.

    An example run might look like:

    .. code-block:: sh

        $ python main.py
        Floaty number [5.0]:
        Number: 5

        RESULTS
        number: 5
        floaty_number: 5.0

        Process finished with exit code 0

    Custom prompt messages can be prepended by adding a `doc` entry to the `metadata` dictionary in each
    :py:func:`dataclasses.field` as in:

    .. code-block:: python

        # main.py

        from dataclasses import field
        import click
        from easy_config import EasyConfig
        from easy_config.contrib.click import easy_config_option

        class ExampleConfig(EasyConfig):
            FILES = None
            NAME = 'MyProgram'

            number: int = field(metadata={'doc': 'A number'})
            floaty_number: float = field(5.0, metadata={'doc': 'A floating point number'})
    """

    def decorate(command: G) -> F:  # noqa: D202
        """Decorate the :mod:`click` command."""

        @args_from_config(cls, prompt=prompt)
        def inner_decorate(**kwargs: Any) -> Any:
            """Apply the keyword arguments to the EasyConfig class."""
            return command(cls.load(**kwargs))

        return inner_decorate  # type: ignore

    return decorate


def args_from_config(cls: Type[EasyConfig], prompt: bool = False) -> Callable[[F], F]:  # noqa: D202
    """Build a decorator based on the given easy config class.

    :param cls: An EasyConfig class
    :param prompt: If true, adds prompts to the resulting CLI for all fields.
    """

    def decorate(command: F) -> F:
        """Decorate the :mod:`click` command."""
        for field in reversed(dataclasses.fields(cls)):
            if prompt:
                doc = field.metadata.get('doc') if field.metadata is not None else None
                if doc is not None:
                    prompt_text = f'{doc.rstrip(".")}.\n{field.name.replace("_", " ").capitalize()}'
                else:
                    prompt_text = True  # type: ignore

                wrapper = click.option(
                    f'--{field.name}',
                    type=field.type,
                    prompt=prompt_text,
                    default=None if field.default is dataclasses.MISSING else field.default,
                    show_default=field.default is not dataclasses.MISSING,
                )

            elif field.default is dataclasses.MISSING:
                wrapper = click.argument(field.name, type=field.type)

            else:
                wrapper = click.option(
                    f'--{field.name}',
                    type=field.type,
                    default=field.default,
                    show_default=True,
                )

            command = wrapper(command)  # type: ignore

        return command

    return decorate
