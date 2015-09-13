#!/usr/bin/env python

from hawkeyapi.database import Teams, TeamAltnames
from hawkeyapi.factories import TeamFactory

#b_team = Teams.get_item(id='NCAA-RIT-W')
#b_team['altnames'] = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']
#b_team.save()

team_id = 'NCAA-Harvard-W'
new_altname = 'HARVARD'

t_db = Teams.get_item(id=team_id)
t_obj = TeamFactory.make(t_db)

TeamAltnames.put_item(data={
    'team_id': team_id,
    'altname': new_altname,
    'is_women': t_obj.is_women,
    'league': t_obj.league,
},
overwrite=True)

alts = TeamAltnames.query_2(team_id__eq=team_id)
print [t['altname'] for t in alts]
