#!/usr/bin/env python

from hawkeyapi.database import Teams
from hawkeyapi.factories import TeamFactory

team_items = Teams.query_2(
    index='Conference-Id-Index',
    home_conference__eq='ECAC',
    is_women__eq=True,
)

for t_db in team_items:
    print t_db['id']
