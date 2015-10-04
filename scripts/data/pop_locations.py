#!/usr/bin/env python

from hawkeyapi.database import Locations

Locations.put_item(data={
    'id': 'WALTER BROWN ARENA',
    'cn': 'Walter Brown Arena',
    'street': '285 BABCOCK ST',
    'city': 'BOSTON',
    'state': 'MA',
    'postal': '02215',
    'country': 'USA',
}, overwrite=True)

Locations.put_item(data={
    'id': 'ALFOND',
    'cn': 'Alfond Arena',
    'street': 'TUNK RD',
    'city': 'ORONO',
    'state': 'ME',
    'postal': '04473',
    'country': 'USA',
}, overwrite=True)

Locations.put_item(data={
    'id': 'SCHNEIDER',
    'cn': 'Schneider Arena',
    'street': '292 HUXLEY AVE',
    'city': 'PROVIDENCE',
    'state': 'RI',
    'postal': '02908',
    'country': 'USA',
}, overwrite=True)
