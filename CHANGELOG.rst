Changelog
=========

Changes as of 10 February 2019

1.0.0 <11 February 2019>
^^^^^^^^^^^^^^^^^^^^^^^^
- Stabilization and 1.0.0 release!
- Add docs
- Use `ChainMap` instead of repeated `dict.update`'s in the loading code (@cthoyt)
- Add Click integration under `easy_config.contrib.click` (@cthoyt)
- Improve error messages when configuration value strings cannot be used to create configuration values of the appropriate type
- Change names of `_load_*` private methods to `_read_*` to better indicate their purpose
- Raise `TypeError` instead of `NotImplementedError` in the base `EasyConfig.__init__` to improve behavior in PyCharm and possibly other IDEs

0.2.0 <26 September 2018>
^^^^^^^^^^^^^^^^^^^^^^^^^
- Add `contrib` package for containing functionality that interacts with other packages, especially those outside the stdlib (@cthoyt)
- Add `click` extension to the contrib package for creating a `click` decorator based on an `EasyConfig` instance (@cthoyt)

0.1.0 <25 September 2018>
^^^^^^^^^^^^^^^^^^^^^^^^^
- Initial beta release to PyPI
- Implementation of most planned functionality
- 100% test coverage
- Clean bill of health from the various linters and MyPy
- Loading of file specified by an environment variable (@cthoyt)
