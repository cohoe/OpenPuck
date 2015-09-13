#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Seasons
from hawkeyapi.util import get_uncombined_timestamp
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
season = SeasonFactory.make(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
entries = ScheduleEntries.query_2(
    team_id__eq='NCAA-Yale-W'
)

for e_db in entries:
    e_myid = e_db['id']
    e_obj = ScheduleEntryFactory.make(e_db)
    print e_obj.json()
