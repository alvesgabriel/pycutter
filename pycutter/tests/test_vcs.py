import os
import pytest
import shutil

from pycutter.command import vcs


@pytest.fixture
def directory():
    dirname = "/tmp/xpto"
    yield dirname
    shutil.rmtree(dirname)


def test_create_dir(directory):
    vcs.create_dir(directory)
    assert os.path.isdir(directory)


def test_gitignore(directory):
    vcs.create_dir(directory)
    vcs.gitignore(directory)
    gitignore = os.path.join(directory, ".gitignore")
    assert os.path.isfile(gitignore)
    assert os.path.getsize(gitignore)


def test_git_init(directory):
    vcs.create_dir(directory)
    vcs.git_init(directory)
    git_dir = os.path.join(directory, ".git")
    assert os.path.isdir(git_dir)
