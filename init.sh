#! /bin/bash

pip install -r requirements.txt
pip install requests
python manage.py migrate

export PYTHONPATH=.
python util/clean_matches.py 0
python util/clean_pick.py
python util/create_heros.py

bash update_DB.sh
