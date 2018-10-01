Changelog
=========

Changes as of 25 September 2018

0.2.1-dev
^^^^^^^^^
- Add docs
- Use `ChainMap` instead of repeated `dict.update`'s in the loading code (@cthoyt)


0.2.0 <26 September 2018>
^^^^^^^^^^^^^^^^^^^^^^^^^
- Add `contrib` package for containing functionality that interacts with other pacakges, especially those outside the stdlib (@cthoyt)
- Add `click` extension to the contrib pacakge for creating a `click` decorator based on an `EasyConfig` instance (@cthoyt)

0.1.0 <25 September 2018>
^^^^^^^^^^^^^^^^^^^^^^^^^

- Initial beta release to PyPI
- Implementation of most planned functionality
- 100% test coverage
- Clean bill of health from the various linters and MyPy
- Loading of file specified by an environment variable (@cthoyt)
