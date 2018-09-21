import configparser
import dataclasses
import logging
import os
from distutils.util import strtobool
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, TextIO, Type, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='EasyConfig')


class _InheritDataclassForConfig(type):
    REQUIRED_CLASS_VARIABLES = ['FILES', 'NAME']

    def __new__(meta, name, bases, attrs):
        for varname in meta.REQUIRED_CLASS_VARIABLES:
            if varname not in attrs:
                logger.debug('required class variable `%s` not present for new class `%s`; not decorating as dataclass', varname, name)
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
            try:
                if field.type is int:
                    value = config.getint(cls.NAME, field.name)
                elif field.type is float:
                    value = config.getfloat(cls.NAME, field.name)
                elif field.type is bool:
                    value = config.getboolean(cls.NAME, field.name)
                else:
                    value = field.type(config.get(cls.NAME, field.name))

                values[field.name] = value
            except (configparser.NoSectionError, configparser.NoOptionError):
                pass

        return values

    @classmethod
    def _load_environment(cls: Type[T]) -> Dict[str, Any]:
        # load from the environment
        values = {}
        for field in dataclasses.fields(cls):
            prefixed_field_name = f'{cls.NAME}_{field.name}'.upper()
            if prefixed_field_name in os.environ:
                if field.type is bool:
                    values[field.name] = field.type(strtobool(os.environ[prefixed_field_name]))
                else:
                    values[field.name] = field.type(os.environ[prefixed_field_name])

        return values

    @classmethod
    def _load_dict(cls: Type[T], d: Dict[str, Any]) -> Dict[str, Any]:
        # load from a dictionary
        return {
            field.name: field.type(d[field.name])
            for field in dataclasses.fields(cls)
            if field.name in d
        }

    @classmethod
    def load(cls: Type[T], additional_files: Optional[Iterable[Union[Path, TextIO]]]=None, *, parse_files: bool=True, parse_environment: bool=True, **kwargs) -> T:
        values = {}
        if parse_files and cls.FILES:
            for f in cls.FILES:
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
