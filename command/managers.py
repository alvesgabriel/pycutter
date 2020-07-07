import os
import subprocess
import venv


class Manager:
    packages_default = "requests".split()


class Pip(Manager):
    name = "pip"

    def __init__(self, directory=os.getcwd()):
        self.directory = directory
        self.project = self.directory.split("/")[-1]
        self.env_dir = os.path.join(self.directory, ".venv")

    def create_venv(self):
        if not os.path.isdir(self.env_dir):
            venv.create(self.env_dir, prompt=self.project)
        self._install_packages()

    def _install_packages(self):
        python = os.path.join(self.env_dir, "bin", "python")
        reqs = subprocess.check_output(
            [python, "-m", self.name, "install", *self.packages_default]
        ).decode("utf-8")
        success = "Successfully installed "
        if success in reqs:
            libs = reqs.split(success)[-1].split(" ")
            print(libs)
