from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def example_ini(tmpdir_factory) -> Path:
    example_ini_contents = """[MyProgram]\n# comment\nnumber = 3"""
    example_ini_path = tmpdir_factory.mktemp('config').join('example.ini')
    with open(example_ini_path, 'w') as f:
        f.write(example_ini_contents)
    return Path(example_ini_path)
