# {{ cookiecutter.project_title }}

{{ cookiecutter.description }}

<p align="center">
  <a href="https://github.com/ambv/black"><img
    src="https://img.shields.io/badge/code%20style-black-000000.svg"
    alt="Code Style"
  /></a>
  <!-- <a href="https://github.com/github-username/repo/actions"><img
    src="https://github.com/github-username/repo/actions/workflows/workflow-name/badge.svg"
    alt="Build"
  /></a> -->
  <!-- <a href="https://github.com/github-username/repo/blob/main/LICENSE"><img
    src="https://img.shields.io/github/license/github-username/repo"
    alt="LICENSE"
  /></a> -->
</p>

## Local Development

## Basic Commands

### Setting Up Your Users

- Run the following command to make migrations then migrate:

        $ python manage.py makemigrations
        $ python manage.py migrate

- To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

- Enter your email address and password.
- Now you can login and view admin panel. Go to http://127.0.0.1:8000/admin and login.

### Type checks

Running type checks with mypy:

    $ mypy .

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Check linting and run pre-commit check

Run the following command on your shell:

> Make sure you have initialized a git repository

    $ pre-commit run --all-files
