#! /bin/bash

pip install -r requirements.txt
pip install requests
python manage.py migrate

python clean_matches.py 0
python clean_pick.py
python create_heros.py
python create_matches.py

