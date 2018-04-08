#! /bin/bash

export PYTHONPATH=.
python util/create_matches.py
python util/create_pick_seq.py

