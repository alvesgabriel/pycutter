import os

import click
import git

APP_NAME = "pycutter"


@click.command()
@click.option("-d", "--directory", default=os.getcwd(), help="Project directory")
def main(directory):
    """
    Cookiecutter CLI to start projects Python
    """
    print("Start project")
    create_dir(directory)


def create_dir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    git_init(directory)


def git_init(directory):
    git_dir = os.path.join(directory, ".git")
    if not os.path.isdir(git_dir):
        g = git.cmd.Git(directory)
        g.init()


if __name__ == "__main__":
    main()
