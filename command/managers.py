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
            venv.create(self.env_dir, prompt=self.project, with_pip=True)

    def install_packages(self, packages):
        python = os.path.join(self.env_dir, "bin", "python")
        reqs = subprocess.check_output(
            [python, "-m", self.name, "install", *packages]
        ).decode("utf-8")
        success = "Successfully installed "
        if success in reqs:
            return reqs.split(success)[-1].strip("\n").split(" ")

    def write_requirements(self, libs, filename="requirements.txt"):
        file_requirements = os.path.join(self.directory, filename)
        with open(file_requirements, "a") as f:
            for lib in libs:
                index = lib.rfind("-")
                dependence = f"{lib[:index]}=={lib[index+1:]}\n"
                f.write(dependence)
