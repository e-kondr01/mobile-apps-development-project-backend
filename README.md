# Проект по предмету "Разработка мобильных приложений"

Бэкенд на Django Rest Framework.

## Python version
3.10

## Local
### Installation
#### Django app
1. Create venv
```bash
python3.10 -m venv .venv
```

2. Activate venv
```bash
source .venv/bin/activate
```

3. Install requirements
```bash
pip install -r app/requirements/local.txt
```

4. Copy .env
```bash
cp app/app/local.example.env app/app/.env
```

5. Set Django's secret key and params to access 1C in .env

#### Docker and Docker compose
Refer to:

https://docs.docker.com/engine/install/

### Usage

1. Use the script to start PSQL in Docker Compose, apply migrations and run development server:
```bash
make local
```

2. To run Celery Beat for periodic tasks, use:
```bash
cd app && celery -A app worker -B -l INFO
```

## Swagger Docs
Go to http://127.0.0.1:8000/api/docs after running server

## Development

During development, use Black formatter, Pylint and Flake8.

## Prod

### Installation
1. Copy .env:
```bash
cp app/app/production.example.env app/app/.env
```

2. Set Django's secret key and params to access 1C in .env

### Deploy
Use shortcut script:
```bash
make up
```
