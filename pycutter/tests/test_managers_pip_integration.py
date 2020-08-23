import os


def test_create_venv_integration(pip):
    pip.create_venv()
    assert os.path.isdir(pip.venv_dir)
    activate = os.path.join(pip.venv_dir, "bin", "activate")
    assert os.path.exists(activate)
    assert os.path.isfile(activate)


def test_install_packages_integration(pip):
    packs = ["django", "flake8", "pytest", "pytest-cov", "requests"]
    pip.create_venv()
    libs = pip.install_packages(packs)
    assert set(packs).issubset([lib[0] for lib in libs])


def test_install_packages_prod_integration(pip):
    pip.create_venv()
    pip.packages = ["requests"]
    libs = pip.install_packages_prod()
    assert set(pip.packages).issubset([lib[0] for lib in libs])


def test_install_packages_dev_integration(pip):
    pip.create_venv()
    pip.packages = ["flake8"]
    libs = pip.install_packages_prod()
    assert set(pip.packages).issubset([lib[0] for lib in libs])


def test_write_requirements_file(pip):
    pip.create_venv()
    filename = "requirements.txt"
    pip.write_requirements_file([("requests", "2.24.0")], filename=filename)
    requirements_file = os.path.join(pip.directory, filename)
    assert os.path.isfile(requirements_file)


def test_write_requirements_file_dev(pip):
    pip.create_venv()
    filename = "requirements-dev.txt"
    libs = [
        ("pytest", "6.0.1"),
        ("pytest-cov", "2.10.1"),
        ("pytest-mock", "3.2.0"),
    ]
    pip.write_requirements_file(libs, filename=filename, dev=True)
    requirements_file = os.path.join(pip.directory, filename)
    with open(requirements_file) as f:
        assert "-r requirements.txt" in f.read()


def test_write_flake8_file(pip):
    pip.create_venv()
    pip.write_flake8_file()
    flake8_file = os.path.join(pip.directory, ".flake8")
    assert os.path.isfile(flake8_file)
