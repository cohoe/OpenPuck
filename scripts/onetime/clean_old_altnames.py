#!/usr/bin/env python

from hawkeyapi.database import Teams, TeamAltnames

#all_teams = Teams.scan()
#
#for team in all_teams:
#    del team['altnames']
#    team.save()

for name in TeamAltnames.scan():
    del name['league']
    name.save()
