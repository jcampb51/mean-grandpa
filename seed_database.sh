#!/bin/bash

rm db.sqlite3
rm -rf ./grandpaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations grandpaapi
python3 manage.py migrate grandpaapi
# python3 manage.py loaddata users
# python3 manage.py loaddata tokens
python manage.py loaddata users.json
python manage.py loaddata tokens.json
python manage.py loaddata category.json
python manage.py loaddata exercise.json
python manage.py loaddata exercisecategory.json
python manage.py loaddata kudo.json
python manage.py loaddata workout.json
python manage.py loaddata workoutcategory.json
python manage.py loaddata workoutexercise.json

