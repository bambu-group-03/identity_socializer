# identity_socializer

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m identity_socializer
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Configuration

This application can be configured with environment variables.

```bash
cp .env_template .env
```

CREATE NETWORK BTW MICROSERVICES

```bash
docker network create -d bridge microservices
```

All environment variables should start with "IDENTITY_SOCIALIZER_" prefix.

For example if you see in your "identity_socializer/settings.py" a variable named like
`random_parameter`, you should provide the "IDENTITY_SOCIALIZER_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `identity_socializer.settings.Settings.Config`.

An example of .env file:

```bash
IDENTITY_SOCIALIZER_RELOAD="True"
IDENTITY_SOCIALIZER_PORT="8000"
IDENTITY_SOCIALIZER_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Docker

You can start the project with docker using this command:

```bash
docker compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "identity_socializer"
identity_socializer
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

-   black (formats your code);
-   mypy (validates types);
-   isort (sorts imports in all files);
-   flake8 (spots possible bugs);

You can read more about pre-commit here: https://pre-commit.com/

## Kubernetes

To run your app in kubernetes
just run:

```bash
kubectl apply -f deploy/kube
```

It will create needed components.

If you haven't pushed to docker registry yet, you can build image locally.

```bash
docker compose -f deploy/docker-compose.yml --project-directory . build
docker save --output identity_socializer.tar identity_socializer:latest
```

## Migrations

If you want to migrate your database, you should run following commands:

```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=identity_socializer" -e "POSTGRES_USER=identity_socializer" -e "POSTGRES_DB=identity_socializer" postgres:13.8-bullseye
```

2. Run the pytest.

```bash
pytest -vv .
```
