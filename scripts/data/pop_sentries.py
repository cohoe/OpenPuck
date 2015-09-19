#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries, Seasons
from hawkeyapi.factories import TeamFactory, SeasonFactory, ScheduleEntryFactory

team_entries = [
    Teams.get_item(id='NCAA-Harvard-W'),
    Teams.get_item(id='NCAA-Yale-W'),
    #Teams.get_item(id='NCAA-UConn-W'),
]

#team_entries = Teams.scan(is_women__eq=True, league__eq='NCAA')

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
s_obj = SeasonFactory.objectify(s_db)

for t_db in team_entries:
    t_obj = TeamFactory.objectify(t_db)

    try:
        entries = t_obj.get_provider().get_schedule(s_obj)
        for e in entries:
            sched_entry = ScheduleEntryFactory.itemify(ScheduleEntries, e)
            sched_entry.save(overwrite=True)
        print "SUCCESS on %s (%i entries)" % (t_obj.id, len(entries))
    except Exception as e:
        print "FAILED on %s" % t_obj.id
        print e
