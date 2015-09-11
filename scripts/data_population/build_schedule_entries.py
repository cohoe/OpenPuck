#!/usr/bin/env python

from hawkeyapi.models import ScheduleEntryModel

if ScheduleEntryModel.exists():
    ScheduleEntryModel.delete_table()

ScheduleEntryModel.create_table()
print "Created schedule_entries table"
