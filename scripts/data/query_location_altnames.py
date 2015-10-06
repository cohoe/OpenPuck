#!/usr/bin/env python

from hawkeyapi.database import Locations, LocationAltnames

b_query = LocationAltnames.query(index='AltnameIndex', altname__eq='BOSTON MASS')
for result in b_query:
    print result['affiliation']
