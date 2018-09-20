import configparser
import dataclasses
import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, TextIO, Type, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='EasyConfig')

class _InheritDataclassForConfig(type):
    REQUIRED_CLASS_VARIABLES = ['PRIORITY']

    def __new__(meta, name, bases, attrs):
        for varname in meta.REQUIRED_CLASS_VARIABLES:
            if not varname in attrs:
                logger.debug('required class variable `%s` not present; not decorating as dataclass', varname)
                break
        else:  # nobreak--nothing was missing
            return dataclasses.dataclass(super().__new__(meta, name, bases, attrs))

        # did break--something was missing
        return super().__new__(meta, name, bases, attrs)


class EasyConfig(metaclass=_InheritDataclassForConfig):
    def __init__(self):
        raise NotImplementedError(f'{self.__class__.__qualname__} must be subclassed')

    @classmethod
    def _load_file(cls: Type[T], config_file: Union[Path, TextIO]) -> Dict[str, Any]:
        # Load a file
        # Default using configparser, but override this to add other file types
        config = configparser.ConfigParser()
        if isinstance(config_file, Path) or isinstance(config_file, str):
            config.read(config_file)
        else:
            config.read_file(config_file)

        values = {}
        for field in dataclasses.fields(cls):
            if field.type is int:
                value = config.getint('default', field.name)
            elif field.type is float:
                value = config.getfloat('default', field.name)
            elif field.type is bool:
                value = config.getboolean('default', field.name)
            else:
                value = config.get('default', field.name)

            values[field.name] = value

        return values

    @classmethod
    def _load_environment(cls: Type[T]) -> Dict[str, Any]:
        # load from the environment
        values = {}
        for field in dataclasses.fields(cls):
            if field.name in os.environ:
                values[field.name] = field.type(os.environ[field.name])

        return values

    @classmethod
    def _load_dict(cls: Type[T], d: Dict[str, Any]) -> Dict[str, Any]:
        # load from a dictionary
        values = {}
        for field in dataclasses.fields(cls):
            if field.name in d:
                values[field.name] = field.type(d[field.name])
        return values

    @classmethod
    def load(cls: Type[T], additional_files: Optional[Iterable[Union[Path, TextIO]]]=None, *, parse_files: bool=True, parse_environment: bool=True, **kwargs) -> T:
        values = {}
        if parse_files:
            for f in cls.files:
                values.update(cls._load_file(f))
        if additional_files:
            for f in additional_files:
                values.update(cls._load_file(f))
        if parse_environment:
            values.update(cls._load_environment())
        values.update(cls._load_dict(kwargs))

        try:
            return cls(**values)
        except TypeError as e:
            if e.args[0].startswith('__init__() missing'):
                raise TypeError('missing some configuration values') from e
            else:
                raise e

    def dump(self):
        # Write current config to a file or something
        pass

    def dumps(self):
        # Return current config as a string
        pass

