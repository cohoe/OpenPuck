#!/usr/bin/env python

from hawkeyapi.database import Teams
from hawkeyapi.objects import Team

item = Teams.get_item(id='NCAA-RIT-W')
#print item['id']

teams = Teams.query_2(
    index='Conference-Id-Index',
    home_conference__eq='CHA',
    is_women__eq=True,
)

for t in teams:
    print t['id']
    team = Team(
        t['institution'],
        t['mascot'],
        t['is_women'],
        t['home_conference'],
        t['social_media'],
        t['web_site'],
        t['web_provider'],
    )

    print team.json()
