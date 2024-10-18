#!/bin/bash

rm db.sqlite3
rm -rf ./grandpaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations grandpaapi
python3 manage.py migrate grandpaapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

