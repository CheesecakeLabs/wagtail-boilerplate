# Mão na Massa Website

## Developing and running locally

### Tab 1:

Prepare:
```bash
cd src/static
yarn install
```

Run:
```bash
yarn dev
```

### Tab 2:

Duplicate `local.example.env` and raname to `local.env`. Comment-out DATABASE_URL if you want to
use default SQLite.

Prepare:
```bash
pip install -r requirements.txt
flake8 --install-hook git
```

Run:
```bash
python manage.py migrate
python src/manage.py runserver
```

**Note**: if you want to use Postgres, run `docker-compose up db`.


## Deploying

TBD
