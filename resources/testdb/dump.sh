#!/bin/bash

tables='games location_altnames locations schedule_entries season_phases seasons team_altnames teams'

for t in $tables; do
    echo $t
    dynamodb-dumper -o http://localhost:8000 $t
done
