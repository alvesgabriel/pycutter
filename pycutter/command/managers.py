import os
import subprocess
import venv

import click

from . import TAB2


class Manager:
    def __init__(self, packages=None, packages_dev=None):
        if packages is None:
            packages = "django"
        if packages_dev is None:
            packages_dev = "flake8 pytest pytest-cov"
        self.packages = packages
        self.packages_dev = packages_dev

    def config_pyup(directory):
        file_pyup = os.path.join(directory, ".pyup.yml")
        with open(file_pyup, "w") as f:
            f.writelines(
                [
                    "requirements:\n",
                    f"{TAB2}- requirements.txt\n",
                    f"{TAB2}- requirements-dev.txt\n",
                ]
            )


class Pip(Manager):
    name = "pip"

    def __init__(self, directory=os.getcwd(), packages=None, packages_dev=None):
        self.directory = directory
        self._project = self.directory.split("/")[-1]
        self.venv_dir = os.path.join(self.directory, ".venv")
        super().__init__(packages, packages_dev)

    def create(self):
        click.echo("Creating venv")
        self.create_venv()

        click.echo("Instaling libs: %s" % ", ".join(self.packages))
        libs = self.install_packages(self.packages)

        click.echo("Writing requirements.txt")
        self.write_requirements_file(libs)

        click.echo("Instaling libs dev: %s" % ", ".join(self.packages_dev))
        libs_dev = self.install_packages(self.packages_dev)

        click.echo("Writing requirements.txt")
        self.write_requirements_file(
            libs_dev, filename="requirements-dev.txt", dev=True
        )

        click.echo("Writing .flake8")
        self.write_flake8_file()

    def create_venv(self):
        if not os.path.isdir(self.venv_dir):
            venv.create(self.venv_dir, prompt=self._project, with_pip=True)

    def install_packages(self, packages):
        python = os.path.join(self.venv_dir, "bin", "python")
        reqs = subprocess.check_output(
            [python, "-m", self.name, "install", *packages]
        ).decode("utf-8")
        success = "Successfully installed "
        if success in reqs:
            libs = reqs.split(success)[-1].strip("\n").split(" ")
            return [tuple(lib.rsplit("-", 1)) for lib in libs]

    def install_packages_prod(self):
        return self.install_packages(self.packages)

    def install_packages_dev(self):
        return self.install_packages(self.packages_dev)

    def write_requirements_file(self, libs, filename="requirements.txt", dev=False):
        file_requirements = os.path.join(self.directory, filename)
        with open(file_requirements, "w+b") as f:
            if dev and not f.readlines():
                f.write(b"-r requirements.txt\n\n")
            [f.write(f"{lib[0]}=={lib[1]}\n".encode()) for lib in libs]

    def write_flake8_file(self, line_length=120):
        file_flake8 = os.path.join(self.directory, ".flake8")
        with open(file_flake8, "w") as f:
            f.writelines(
                ("[flake8]\n", f"max-line-length={line_length}\n", "exclude=.venv\n")
            )
