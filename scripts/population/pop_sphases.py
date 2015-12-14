#!/usr/bin/env python

from hawkeyapi.database import SeasonPhases
from datetime import date

SeasonPhases.put_item(data={
    'id': 'NCAA-1415-W',
    'name': 'ConferencePlay',
    'start': date(2014, 10, 3).toordinal(),
    'end': date(2015, 2, 20).toordinal(),
},
overwrite=True)

SeasonPhases.put_item(data={
    'id': 'NCAA-1415-W',
    'name': 'ConferenceTournament',
    'start': date(2015, 2, 27).toordinal(),
    'end': date(2015, 3, 8).toordinal(),
},
overwrite=True)

SeasonPhases.put_item(data={
    'id': 'NCAA-1415-W',
    'name': 'LeagueTournament',
    'start': date(2015, 3, 13).toordinal(),
    'end': date(2015, 3, 25).toordinal(),
},
overwrite=True)
