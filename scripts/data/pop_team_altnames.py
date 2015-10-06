#!/usr/bin/env python

from hawkeyapi.database import Teams, TeamAltnames

t_entries = Teams.scan()
for team in t_entries:
    TeamAltnames.put_item(data={
        'team_id': team['id'],
        'altname': team['id'],
        'league': team['league'],
        'is_women': team['is_women'],
    },
    overwrite=True)
