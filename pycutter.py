import os

import click
import git

from command.ci import Travis
from command.managers import Pip, config_pyup

APP_NAME = "pycutter"

manager_choices = {
    "pip": Pip(),
}

ci_choices = {
    "travis": Travis(),
}


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
@click.option(
    "-c",
    "--ci",
    default="travis",
    type=click.Choice(("travis",)),
    show_default=True,
    help="Contiuous integration service",
)
@click.option(
    "-p",
    "--pyup",
    is_flag=True,
    help="Pyup keep your Python dependencies secure, up-to-date & compliant",
)
def main(directory, manager_package, ci, pyup):
    """
    Cookiecutter CLI to start projects Python
    """
    click.echo("Start project")
    create_dir(directory)
    create_venv(directory)
    ci_choices[ci].config(directory)
    if pyup:
        config_pyup(directory)


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


def create_venv(directory):
    click.echo("Creating venv")
    pip = Pip(directory)
    pip.create_venv()

    click.echo("Instaling libs: %s" % ", ".join(pip.packages_default))
    libs = pip.install_packages(pip.packages_default)

    click.echo("Writing requirements.txt")
    pip.write_requirements_file(libs)

    click.echo("Instaling libs dev: %s" % ", ".join(pip.packages_dev))
    libs_dev = pip.install_packages(pip.packages_dev)

    click.echo("Writing requirements.txt")
    pip.write_requirements_file(libs_dev, filename="requirements-dev.txt", dev=True)

    click.echo("Writing .flake8")
    pip.write_flake8_file()


if __name__ == "__main__":
    main()
