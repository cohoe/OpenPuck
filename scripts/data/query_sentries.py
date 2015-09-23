#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Seasons
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory
from datetime import date

s_db = Seasons.get_item(id='NCAA-1415-W')
season = SeasonFactory.objectify(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
#entries = ScheduleEntries.query_2(
#    team_id__eq='NCAA-Yale-W'
#)

start_date = date(2015, 1, 1).toordinal()
end_date = date(2015, 1, 31).toordinal()

entries = ScheduleEntries.query_2(
    #team_id__eq='NCAA-Yale-W',
    index='LeagueDateIndex',
    league__eq='NCAA',
    date__between=[start_date, end_date],
)

for e_db in entries:
    e_myid = e_db['id']
    e_obj = ScheduleEntryFactory.objectify(e_db)
    print e_obj.json()
