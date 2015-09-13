#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries
from hawkeyapi.objects import ScheduleEntry
from hawkeyapi.util import get_uncombined_timestamp
from hawkeyapi.TestData import seasons

season = seasons[1]

#team = Teams.get_item(id='NCAA-Yale-W')
entries = ScheduleEntries.query_2(
    #index='ScheduleEntries-TeamId-Index',
    team_id__eq='NCAA-Yale-W'
)

for e_db in entries:
    e_myid = e_db['id']
    [date, time] = get_uncombined_timestamp(e_db['timestamp'])
    e_obj = ScheduleEntry(
        e_db['entry_id'],
        date,
        time,
        e_db['opponent'],
        e_db['site'],
        e_db['location'],
        e_db['links'],
        e_db['is_conference'],
        season
    )

    print e_obj.json()
