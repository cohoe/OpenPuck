#!/usr/bin/env python

from hawkeyapi.database import Seasons

Seasons.put_item(data={
    'id': 'NCAA-1415-W',
    'league': 'NCAA',
    'start': 2014,
    'end': 2015,
    'is_women': True,
},
overwrite=True)

Seasons.put_item(data={
    'id': 'NCAA-1314-W',
    'league': 'NCAA',
    'start': 2013,
    'end': 2014,
    'is_women': True,
},
overwrite=True)

Seasons.put_item(data={
    'id': 'NCAA-1516-W',
    'league': 'NCAA',
    'start': 2015,
    'end': 2016,
    'is_women': True,
},
overwrite=True)
