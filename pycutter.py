import os

import click
import git

from command.managers import Pip

APP_NAME = "pycutter"


@click.command()
@click.option("-d", "--directory", default=os.getcwd(), help="Project directory")
@click.option(
    "-m",
    "--manager-package",
    default="pip",
    type=click.Choice(("pip",)),
    show_default=True,
    help="manager package to install dependences",
)
def main(directory, manager_package):
    """
    Cookiecutter CLI to start projects Python
    """
    click.echo("Start project")
    create_dir(directory)
    Pip(directory).create_venv()


def create_dir(directory):
    if not os.path.isdir(directory):
        click.echo(f"Creating directory: {directory}")
        os.makedirs(directory)
    git_init(directory)


def git_init(directory):
    git_dir = os.path.join(directory, ".git")
    if not os.path.isdir(git_dir):
        click.echo("Inicializing Git")
        g = git.cmd.Git(directory)
        g.init()
        gitignore(directory)


def gitignore(directory):
    file_gitignore = os.path.join(directory, ".gitignore")
    if not os.path.isfile(file_gitignore):
        click.echo("Creating file .gitignore")
        from shutil import copyfile

        app_dir = os.path.dirname(os.path.realpath(__file__))
        app_gitignore = os.path.join(app_dir, ".gitignore")
        copyfile(app_gitignore, file_gitignore)


if __name__ == "__main__":
    main()
