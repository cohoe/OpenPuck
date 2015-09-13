#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries

item = ScheduleEntries.get_item(
    team_id='NCAA-Harvard-W',
    timestamp='2014-10-17T00:00:00',
)

print item['opponent']

print ScheduleEntries.delete_item(
    team_id='NCAA-Harvard-W',
    timestamp='2014-10-17T00:00:00',
)
