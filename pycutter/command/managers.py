import os
import subprocess
import venv

from . import TAB2


class Manager:
    packages_default = "requests".split()
    packages_dev = "flake8".split()


class Pip(Manager):
    name = "pip"

    def __init__(self, directory=os.getcwd()):
        self.directory = directory
        self.project = self.directory.split("/")[-1]
        self.env_dir = os.path.join(self.directory, ".venv")

    def create_venv(self):
        if not os.path.isdir(self.env_dir):
            venv.create(self.env_dir, prompt=self.project, with_pip=True)

    def install_packages(self, packages):
        python = os.path.join(self.env_dir, "bin", "python")
        reqs = subprocess.check_output(
            [python, "-m", self.name, "install", *packages]
        ).decode("utf-8")
        success = "Successfully installed "
        if success in reqs:
            return reqs.split(success)[-1].strip("\n").split(" ")

    def write_requirements_file(self, libs, filename="requirements.txt", dev=False):
        if libs:
            file_requirements = os.path.join(self.directory, filename)
            with open(file_requirements, "w+b") as f:
                if dev and not f.readlines():
                    f.write(b"-r requirements.txt\n\n")
                for lib in libs:
                    index = lib.rfind("-")
                    dependence = f"{lib[:index]}=={lib[index+1:]}\n"
                    f.write(dependence.encode())

    def write_flake8_file(self, line_length=120):
        file_flake8 = os.path.join(self.directory, ".flake8")
        with open(file_flake8, "w") as f:
            f.writelines(
                ("[flake8]\n", f"max-line-length={line_length}\n", "exclude=.venv\n")
            )


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