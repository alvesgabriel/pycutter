import os
import pytest
import shutil

from pycutter.command import vcs


@pytest.fixture
def make_dir():
    dirname = "/tmp/xpto"
    yield dirname
    shutil.rmtree(dirname)


def test_create_dir(make_dir):
    vcs.create_dir(make_dir)
    assert os.path.isdir(make_dir)
