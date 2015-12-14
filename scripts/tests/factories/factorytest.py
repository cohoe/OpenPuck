#!/usr/bin/env python

from hawkeyapi.factories import TeamFactory, ScheduleEntryFactory, SeasonFactory
from hawkeyapi.database import Teams, ScheduleEntries, Seasons

t_db = Teams.get_item(id='NCAA-RIT-W')
t_obj = TeamFactory.objectify(t_db)
print t_obj.json()

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
s_obj = SeasonFactory.objectify(s_db)
print s_obj.json()

se_db = ScheduleEntries.get_item(team_id='NCAA-Harvard-W', date='2014-10-17')
se_obj = ScheduleEntryFactory.objectify(se_db)
print se_obj.json()
