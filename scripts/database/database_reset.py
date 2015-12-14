#!/usr/bin/env python

from hawkeyapi.database import Teams, Seasons, SeasonPhases

for db in [Teams, Seasons, SeasonPhases]:
    items = Teams.scan()
    for i in items:
        i.delete()
