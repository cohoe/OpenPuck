#!/usr/bin/env python

from hawkeyapi.models import TeamModel
from hawkeyapi.objects import Team

#entries = TeamModel.query(home_conference__eq='CHA')
#entries = TeamModel.scan()
#entries = TeamModel.query('Northeastern University', is_women__eq=True)
#entries = TeamModel.query('Northeastern University')
entries = TeamModel.conference_index.query('HEA', is_women__eq=True)
for e in entries:
    print e.name
    t = Team(
        e.name,
        e.mascot,
        e.is_women,
        e.home_conference,
        e.social_media,
        e.web_site,
        e.web_provider,
    )

    print t.json()

#entry = TeamModel.get('Northeastern University', True)
#print entry.dumps()
#print entry.name
#print entry.is_women
#print entry.web_site
