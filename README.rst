easy_config
===========
Parse configuration values from files, the environment, and elsewhere all in one place.

|python_versions| |license| |develop_build| |develop_coverage| |develop_docs|

.. |python_versions| image:: https://img.shields.io/badge/python->%3D3.6-blue.svg?style=flat-square
    :alt: Supports Python 3.6 and later
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: LICENSE.rst
    :alt: MIT License
.. |develop_build| image:: https://img.shields.io/travis/com/scolby33/easy_config/develop.svg?style=flat-square
    :target: https://travis-ci.com/scolby33/easy_config
    :alt: Develop Build Status
.. |develop_coverage| image:: https://img.shields.io/codecov/c/github/scolby33/easy_config/develop.svg?style=flat-square
    :target: https://codecov.io/gh/scolby33/easy_config/branch/develop
    :alt: Develop Test Coverage
.. |develop_docs| image:: https://img.shields.io/readthedocs/easy-config/latest.svg?style=flat-square
    :target: https://easy-config.readthedocs.io/
    :alt: Develop Docs Status

Example
-------

Here is a full working example of using easy_config.
First, write your configuration class:

.. code-block:: python

   # config.py
   from easy_config import EasyConfig

   class MyProgramConfig(EasyConfig):
      FILES = ['myprogram.ini']
      NAME = 'MyProgram'  # the name for the .ini file section and the namespace prefix for environment variables

      # define the options like you would a dataclass
      number: int
      name: str
      check_bounds: bool = True  # options with defaults must all come after non-default options

A sample configuration file:

.. code-block:: ini

   # myprogram.ini
   [MyProgram]
   # section name matches `NAME` from the configuration class
   number = 3

And a sample program to illustrate the usage:

.. code-block:: python

   # test_config.py
   import sys

   from config import MyProgramConfig

   print(MyProgramConfig.load(name=sys.argv[1])

Running this program with various options:

.. code-block:: bash

   $ python test_config.py Scott
   MyProgramConfig(number=3, name='Scott', check_bounds=True)

   $ env MYPROGRAM_CHECK_BOUNDS=False python test_config.py Scott
   # environment variable names are the all-uppercase transformation of the NAME concatenated with the option name and an underscore
   MyProgramConfig(number=3, name='Scott', check_bounds=False)

   $ env MYPROGRAM_NUMBER=10 MYPROGRAM_NAME=Charlie python test_config.py Scott
   MyProgramConfig(number=10, name='Scott', check_bounds=True)

As you can see, values are taken in precedence, with arguments passed to ``load``
overriding values from the environment which, in turn, override values from
configuration files.

Once you have the ``MyProgramConfig`` instance, you can use it just like any dataclass.

