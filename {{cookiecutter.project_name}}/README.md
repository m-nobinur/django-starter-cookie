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

- [{{ cookiecutter.project_title }}](#-cookiecutterproject_title-)
  - [Local Development](#local-development)
  - [Basic Commands](#basic-commands)
    - [Type checks](#type-checks)
    - [Test coverage](#test-coverage)
    - [Running tests with pytest](#running-tests-with-pytest)
    - [Check linting and run pre-commit check](#check-linting-and-run-pre-commit-check)

## Local Development

>❗ Make sure you've python3, pip and node installed on your machine.

- To check your machine meets all the requirements run the following command:
  
```bash
source ./utils/scripts/precheck.sh
```

- Create a folder where to clone the project and cd into it.

```bash
mkdir <folder-name>
```

Install a virtual environment manager if not installed yet. We will use [Pipenv](https://pipenv.readthedocs.io/en/latest/).

1. For installing pipenv run:

    ```bash
    pip install pipenv
    ```

1. Now clone the project and navigate to `{{ cookiecutter.project_name }}` folder.

    ```bash
    git clone <project-github-link>
    ```

1. Activate the virtual environment

    ```bash
    pipenv shell
    ```

1. Install all the local dependencies for the project

    ```bash
    pip install -r requirements/local.txt

    npm install
    ```

1. Make sure to be in the project's root directory and run the following command

    ```bash
    export DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.settings.local

    python ./utils/scripts/autoenv.py
    ```

1. Now run the following command

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

1. Now create a superuser

    ```bash
    python manage.py createsuperuser
    ```

1. To run tailwind jit compiler, start a new terminal session and run

    > Make sure you are in project's root folder.

    ```bash
    npx tailwindcss -i ./static/sass/input.css -o ./static/css/default__main.css
    ```

1. If all gone well you can now start the server

    ```bash
    python manage.py runserver
    ```

1. Now your site is ready to visit. Go to [http://127.0.0.1:8000/] and start hacking.

---

> We have created some scripts to automate the process and some aliases to make the development process easier. These scripts are located in the `utils/scripts` folder.

To use the aliases and scripts run the following command

```bash
source ./utils/scripts/main.sh
```

Now we can just run the following commands to start the development server

```bash
env; mrun
```

## Basic Commands

If you've sourced the main script, then the following command will be available:

| Command   | Description                                            |
| :-------- | :----------------------------------------------------- |
| `run`     | Run development server                                 |
| `mmg`     | Run make migrations                                    |
| `mg`      | Migrate database                                       |
| `suser`   | Create a super user                                    |
| `shell`   | Start a new django shell session                       |
| `dbshell` | Start a SQL shell session                              |
| `newapp`  | Create a new app on project directory.                 |
| `env`     | Create a .env file with default environment variables.  |

### Type checks

Running type checks with mypy:

```bash
mypy .
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

### Running tests with pytest

```bash
pytest
```

### Check linting and run pre-commit check

Run the following command on your shell:

> Make sure you have initialized a git repository

```bash
pre-commit run --all-files
```
