# Run the backend

This is prepare for running the local server for the first time.

### Install PostgreSQL (macOS)

**Homebrew** install

```shell
brew install postgresql
```

Start the service

```shell
brew services start postgresql
```

Initilize

```shell
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

### Install dependencies

### one repository and cd to the repo root

```shell
git clone https://github.com/FlickerSoul/Graphery/
cd Graphery
```

### Install dependencies

- for development

  ```shell
  cd backend
  pipenv install -d  # latest dependencies are managed by pipenv
  ```

- install without pipenv

  ```shell
  cd backend
  pip install -r requirements
  ```

### Set the global variables

- for development

  ```shell
  export PYTHONUNBUFFERED=1;
  export DJANGO_SETTINGS_MODULE=graphery.settings.test;
  export GRAPHERY_NORMAL_LOG_PATH=logs/graphery_normal.log;
  export GRAPHERY_EXECUTION_LOG_PATH=logs/graphery_execution.log;
  ```

  Make sure directory `logs` exists in `/server`

- for production
  make sure the the folder `/var/log/graphery` exists and production settings is installed to `server/graphery/settings/production.py`

### Install PostgreSQL and Redis

For installation of PostgreSQL, please check out this [link](https://www.postgresql.org/download/). After PostgreSQL installed, please create a new role and a database that match your setting file.

For installation of Redis, please checkout this [link](https://redis.io/download)

### Run the server

```shell
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
