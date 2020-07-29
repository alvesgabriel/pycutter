import os
import sys


class Travis:
    def __init__(self):
        version = sys.version_info
        self.python_version = f"{version.major}.{version.minor}"

    def config(self, directory):
        filename = os.path.join(directory, ".travis.yml")
        with open(filename, "w") as f:
            f.writelines(
                [
                    "language: python\n",
                    "python:\n",
                    f"\t- {self.python_version}\n",
                    "install:\n",
                    "\t- pip install -r requirements-dev.txt\n",
                    "script:\n",
                    "\t- flake8\n",
                ]
            )
