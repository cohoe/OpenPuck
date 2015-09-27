#!/bin/bash

set -e

cd ../data

python create_seasons.py
python pop_seasons.py

python create_sphases.py
python pop_sphases.py

python create_teams.py
python pop_teams.py

echo "Done!"
