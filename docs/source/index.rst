.. only:: prerelease

   .. warning:: This is the documentation for a development version of easy_config.

      .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <https://easy-config.readthedocs.io/en/stable/>`_


Welcome to easy_config's documentation!
=======================================
Parse configuration values from files, the environment, and elsewhere all in one place.

|python_versions| |license| |develop_build| |develop_coverage|

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

On this page:

.. contents::
     :local:

Installation
------------

.. toctree::
      :maxdepth: 2
      :hidden:

Installation should be as easy as executing this command in your chosen terminal::

    $ pip install easy_config

The source code for this project is `hosted on Github <https://github.com/scolby33/easy_config>`_.
Downloading and installing from source goes like this::

    $ git clone https://github.com/scolby33/easy_config
    $ cd easy_config
    $ pip install .

If you intend to install in a virtual environment, activate it before running
:code:`pip install`.

:mod:`easy_config` officially supports Python 3.6 and later.

Example Usage
-------------

.. toctree::
      :maxdepth: 2
      :hidden:

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

API Reference
-------------

Information about each function, class, and method is included here.

.. toctree::
      :maxdepth: 2

      reference


Click Integration
-----------------

:mod:`easy_config` ships with a contrib module integrating with `the Click command line interface package. <https://click.palletsprojects.com>`_

.. toctree::
      :maxdepth: 2

      contrib/click


License
-------

.. toctree::
    :maxdepth: 2
    :hidden:

    license

:mod:`easy_config` is licensed under the MIT License, a permissive open-source license.

The full text of the license is available :ref:`here <license>` and in the root of the
source code repository.


Changelog
---------

.. toctree::
    :maxdepth: 2
    :hidden:

    changelog

:mod:`easy_config` adheres to the Semantic Versioning ("Semver") 2.0.0 versioning standard.
Details about this versioning scheme can be found on the `Semver website <http://semver.org/spec/v2.0.0.html>`_.
Versions postfixed with '-dev' are currently under development and those without a
postfix are stable releases.

You are reading the documents for version |release| of :mod:`easy_config`.

Full changelogs can be found on the :ref:`changelog` page.


Indices and tables
------------------

.. toctree::
      :maxdepth: 2
      :hidden:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
