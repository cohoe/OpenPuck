#!/usr/bin/env python

from hawkeyapi.database import Teams
from hawkeyapi.factories import TeamFactory

item = Teams.get_item(id='NCAA-RIT-W')
#print item['id']

teams = Teams.query_2(
    index='ConferenceIndex',
    home_conference__eq='ECAC',
    is_women__eq=True,
)

for t in teams:
    team = TeamFactory.objectify(t)
    print team.id
