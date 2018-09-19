import dataclasses

class _InheritDataclassForConfig(type):
    REQUIRED_CLASS_VARIABLES = ['PRIORITY']

    def __new__(meta, name, bases, attrs):
        if not bases:
            return super().__new__(meta, name, bases, attrs)
        for varname in meta.REQUIRED_CLASS_VARIABLES:
            if not varname in attrs:
                raise RuntimeError(f'{varname} must be a defined class variable')
        return dataclasses.dataclass(super().__new__(meta, name, bases, attrs))


class EasyConfig(metaclass=_InheritDataclassForConfig):
    def __init__(self):
        raise NotImplementedError(f'{self.__class__.__qualname__} must be subclassed')

    @classmethod
    def load(cls):
        # Load config based on PRIORITY
        pass

    def dump(self):
        # Write current config to a file or something
        pass

    def dumps(self):
        # Return current config as a string
        pass

