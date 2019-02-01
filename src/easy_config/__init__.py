# -*- coding: utf-8 -*-

"""Parse configuration values from files, the environment, and elsewhere all in one place."""

import configparser
import dataclasses
import logging
import os
from collections import ChainMap
from distutils.util import strtobool
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
)


# metadata
__version__ = '0.2.1-dev'

__title__ = 'easy_config'
# keep the __description__ synchronized with the package docstring
__description__ = 'Parse configuration values from files, the environment, and elsewhere all in one place.'
__url__ = 'https://github.com/scolby33/easy_config'

__author__ = 'Scott Colby'
__email__ = 'scolby33@gmail.com'

__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018 Scott Colby'

logger = logging.getLogger(__name__)

EasyConfigOrSubclass = TypeVar('EasyConfigOrSubclass', bound='EasyConfig')


class ConfigValueCoercionError(ValueError):
    """Raised when a configuration value cannot be converted to the proper type.

    Example: field type is ``int`` and the value is ``None`` or ``'apple'``.
    """

    pass


class _InheritDataclassForConfig(type):
    REQUIRED_CLASS_VARIABLES = ['FILES', 'NAME']

    def __new__(
        mcs, name: str, bases: Tuple[Type[type]], attrs: Dict[str, Any]  # noqa: N804
    ) -> Type[type]:
        for varname in mcs.REQUIRED_CLASS_VARIABLES:
            if varname not in attrs:
                logger.debug(
                    'required class variable `%s` not present for new class `%s`; not decorating as dataclass',
                    varname,
                    name,
                )
                break
        else:  # nobreak--nothing was missing
            return dataclasses.dataclass(super().__new__(mcs, name, bases, attrs))

        # did break--something was missing
        return super().__new__(mcs, name, bases, attrs)


class EasyConfig(metaclass=_InheritDataclassForConfig):
    """The parent class of all configuration classes."""

    NAME: str
    FILES: List[Union[str, Path]]

    def __init__(self, **_kwargs: Any) -> None:
        """Do not instantiate the base class.

        ``TypeError`` is raised instead of ``NotImplementedError`` to prevent IDEs (namely: PyCharm) from complaining
        that subclasses have not implemented all abstract methods.
        See https://github.com/scolby33/easy_config/issues/19

        :raises TypeError: always; this class must be subclassed
        """
        raise TypeError(f'{self.__class__.__qualname__} must be subclassed')

    @classmethod
    def _read_file(
        cls: Type[EasyConfigOrSubclass], config_file: Union[str, Path, Iterable[str]]
    ) -> Dict[str, Any]:
        """Read configuration values from a file.

        This method parses ConfigParser-style INI files.
        To parse other formats, subclass EasyConfig and override this method.

        :param config_file: the file from which configuration will be read. Note that this can be an Iterable[str],
        which includes open files and TextIO objects.

        :returns: a mapping from string configuration value names to their values
        """
        config = configparser.ConfigParser()
        if isinstance(config_file, (str, Path, os.PathLike)):
            config.read(config_file)
        else:
            config.read_file(config_file)

        values = {}
        for field in dataclasses.fields(cls):
            try:
                value: Any
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
            except (TypeError, ValueError) as e:
                raise ConfigValueCoercionError(f'Could not coerce value for field `{field.name}` to type `{field.type}`') from e

        return values

    @classmethod
    def _read_environment(cls: Type[EasyConfigOrSubclass]) -> Dict[str, Any]:
        """Read configuration values from the environment.

        Configuration values are looked up in the environment by the concatenation of the value name and the NAME class
        variable with an underscore separator.

        For example, the configuration value "number" for an instance with the NAME "myprogram" will be read from the
        environment variable "MYPROGRAM_NUMBER".

        :returns: a mapping from string configuration value names to their values
        """
        values = {}
        for field in dataclasses.fields(cls):
            prefixed_field_name = f'{cls.NAME}_{field.name}'.upper()
            try:
                if field.type is bool:
                    values[field.name] = field.type(
                        strtobool(os.environ[prefixed_field_name])
                    )
                else:
                    values[field.name] = field.type(os.environ[prefixed_field_name])
            except KeyError:  # the variable was not in the environment
                pass
            except (TypeError, ValueError) as e:
                raise ConfigValueCoercionError(f'Could not coerce value for field `{field.name}` to type `{field.type}`') from e

        return values

    @classmethod
    def _read_dict(
        cls: Type[EasyConfigOrSubclass], d: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Read configuration values from a passed-in mapping.

        Configuration values are extracted from the input mapping.
        Only keys in the mapping that are valid configuration values names are returned, others are ignored.

        :param d: the input mapping of string configuration value names to their values
        :returns: a mapping from string configuration value names to their values
        """
        values = {}
        for field in dataclasses.fields(cls):
            try:
                if field.name in d:
                    values[field.name] = field.type(d[field.name])
            except (TypeError, ValueError) as e:
                raise ConfigValueCoercionError(f'Could not coerce value for field `{field.name}` to type `{field.type}`') from e

        return values

    @classmethod
    def load(
        cls: Type[EasyConfigOrSubclass],
        _additional_files: Optional[Iterable[Union[str, Path, TextIO]]] = None,
        *,
        _parse_files: bool = True,
        _parse_environment: bool = True,
        _lookup_config_envvar: Optional[str] = None,
        **kwargs: Any,
    ) -> EasyConfigOrSubclass:
        """Load configuration values from multiple locations and create a new instance of the configuration class with those values.

        Values are read in the following order. The last value read takes priority.

        1. values from the files listed in the FILES class variable, in order
        2. values from files passed in the additional_files parameter, in order
        3. values from the file specified by the config file specified by the environment variable _lookup_config_envvar
        4. values from the environment
        5. values passed as keyword arguments to this method (useful for values specified on the command line)

        :param _additional_files: files to be parsed in addition to those named in the FILES class variable;
         always parsed, no matter the value of the parse_files flag
        :param _parse_files: whether to parse files from the FILES class variable
        :param _parse_environment: whether to parse the environment for configuration values
        :param _lookup_config_envvar: the environment variable that contains the config file location. Like the loading
         from the environment, this value will be uppercased and appended to the program name. For example, the
         _lookup_config_envvar "config" for an instance with the NAME "myprogram" will result in a search for the
         environment variable "MYPROGRAM_CONFIG" for the path to the configuration file.
        :param kwargs: additional keyword arguments are passed through unchanged to the final configuration object

        :returns: an instance of the configuration class loaded with the parsed values
        """
        values = ChainMap(
            *cls._load_helper(
                _additional_files=_additional_files,
                _parse_files=_parse_files,
                _parse_environment=_parse_environment,
                _lookup_config_envvar=_lookup_config_envvar,
                **kwargs,
            )
        )

        try:
            return cls(**values)
        except TypeError as e:
            if e.args[0].startswith('__init__() missing'):
                raise TypeError('missing some configuration values') from e
            else:
                raise e

    @classmethod
    def _load_helper(
        cls: Type[EasyConfigOrSubclass],
        _additional_files: Optional[Iterable[Union[str, Path, TextIO]]] = None,
        *,
        _parse_files: bool = True,
        _parse_environment: bool = True,
        _lookup_config_envvar: Optional[str] = None,
        **kwargs: Any,
    ) -> Iterable[Dict[str, Any]]:
        """Help load the dictionaries in .load()."""
        yield cls._read_dict(kwargs)
        if _parse_environment:
            yield cls._read_environment()
        if _lookup_config_envvar is not None:
            envvar = f'{cls.NAME.upper()}_{_lookup_config_envvar.upper()}'
            file_name = os.environ.get(envvar)
            if file_name:
                yield cls._read_file(file_name)
        if _additional_files:
            for files in _additional_files:
                yield cls._read_file(files)
        if _parse_files and cls.FILES:
            for file_paths in reversed(cls.FILES):
                yield cls._read_file(file_paths)

    def dump(self, fp: TextIO) -> None:
        """Serialize all current configuration values to fp as a ConfigParser-style INI.

        Values will be placed in the section corresponding to the class value NAME.

        :param fp: a write()-supporting file-like object
        """
        config = configparser.ConfigParser()
        config[self.NAME] = dataclasses.asdict(self)
        config.write(fp)
