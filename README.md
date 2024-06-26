# Planetarium Service

API service for planetarium management written on DRF


## Installing using GitHub

Install PostgresSQL and create db

```shell
git clone https://github.com/artemgrishko/planetarium.git
cd planetarium_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DB_HOST = <your db hostname>
set DB_NAME = <your db name>
set DB_USER = <your db username>
set DB_PASSWORD = <your db user password>
set SECRET_KEY = <your secret key>
python manage.py migrate
python manage.py runserver
```

## Run with docker

Docker should be installed

```shell
docker-compose build
docker-compose up
```

## Getting access

<ul>
  <li>create user via /api/user/register</li>
  <li>get access token via /api/user/token</li>
</ul>

## Features

<ul>
  <li>JWT authenticated</li>
  <li>Admin panel /admin/</li>
  <li>Documentation is located at /api/doc/swagger/</li>
  <li>Managing orders and tickets</li>
  <li>Creating astronomy shows with show themes</li>
  <li>Creating planetarium domes</li>
  <li>Adding show sessions</li>
  <li>Filtering astronomy shows and show sessions</li>
</ul>
