#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries

items = ScheduleEntries.query_2(
    team_id__eq="NCAA-Yale-W"
)

for i in items:
    i.delete()
