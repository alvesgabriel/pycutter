import shutil
from tempfile import mkdtemp

import pytest

from pycutter.command.managers import Pip


@pytest.fixture()
def directory():
    directory = mkdtemp()
    yield directory
    shutil.rmtree(directory)


@pytest.fixture
def pip(directory):
    pip_obj = Pip(directory)
    return pip_obj
