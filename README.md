# Pegb E-commerce

## Frontend
https://github.com/unibna/pegb-ecommerce-frontend

## Requirements
- Python 3.11.8
- PostgreSQL
- Redis

## Run project
### Local

- Install requirements
```
    # At root directory
    python -m venv venv
    source ./venv/bin/activee

    # At ./src
    pip install -r requirements.txt
```

- Migrate database
```
    # At ./src
    python manage.py migrate
```

- Run server
```
    # At ./src
    python manage.py runserver
```
