# Run the backend

This is prepare for the first time running the local server.

### Install dependencies

```shell
cd backend
pipenv install # latest dependencies was managed by pipenv
```

### Set the global variables

```shell
export PYTHONUNBUFFERED=1;
export DJANGO_SETTINGS_MODULE=graphery.settings.test;
export GRAPHERY_NORMAL_LOG_PATH=logs/graphery_normal.log;
export GRAPHERY_EXECUTION_LOG_PATH=logs/graphery_execution.log;
```

Make sure directory `logs` exists in `/server`

### Run the server

```shell
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
