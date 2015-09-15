#!/usr/bin/env python

from hawkeyapi.factories import SeasonFactory, TeamFactory
from hawkeyapi.database import Seasons, Teams

#season = Seasons.get_item(league='NCAA', id='2014-15W')
#
#s_obj = SeasonFactory.objectify(season)
#s_item = SeasonFactory.itemify(Seasons, s_obj)
#s_item.save(overwrite=True)

team = Teams.get_item(id='NCAA-RIT-W')

t_obj = TeamFactory.objectify(team)
t_item = TeamFactory.itemify(Teams, team['id'], t_obj)
t_item.save(overwrite=True)
