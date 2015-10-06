#!/usr/bin/env python

from hawkeyapi.database import Teams, TeamAltnames

#b_team = Teams.get_item(id='NCAA-RIT-W')
#b_team['altnames'] = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']
#b_team.save()

b_query = TeamAltnames.query(index='AltnamesGenderIndex', altname__eq='BOSTON UNIVERSITY', is_women__eq=True)
for result in b_query:
    print result['team_id']
