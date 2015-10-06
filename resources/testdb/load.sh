#!/bin/bash

tables='games location_altnames locations schedule_entries season_phases seasons team_altnames teams'

for t in $tables; do
    echo $t
    for f in $(ls $t.*.dump); do
        dynamodb-loader -o http://localhost:8000 $t -l $f
    done
done
