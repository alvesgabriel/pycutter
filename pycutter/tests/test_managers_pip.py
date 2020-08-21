import pytest

from unittest.mock import Mock


@pytest.fixture
def venv(mocker):
    return mocker.patch("pycutter.command.managers.venv.create")


def test_create_venv(mocker, pip, venv):
    pip.create_venv()
    venv.assert_called_once_with(pip.venv_dir, prompt=pip._project, with_pip=True)


@pytest.mark.parametrize(
    "pack", [["django"], ["flake8"], ["pytest", "pytest-cov"], ["requests"]]
)
def test_install_packages(pack):
    pip_mock = Mock()
    pip_mock.install_packages.return_value = [
        ("django", "3.1.0"),
        ("flake8", "3.8.3"),
        ("pytest", "6.0.1"),
        ("pytest-cov", "2.10.1"),
        ("pytest-mock", "3.2.0"),
        ("requests", "2.24.0"),
    ]
    pip_mock.create_venv()
    libs = pip_mock.install_packages(pack)
    assert set(pack).issubset([lib[0] for lib in libs])
