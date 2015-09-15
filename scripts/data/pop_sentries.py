#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries, Seasons
from hawkeyapi.factories import TeamFactory, SeasonFactory, ScheduleEntryFactory

team_entries = [
    Teams.get_item(id='NCAA-Harvard-W'),
    Teams.get_item(id='NCAA-Yale-W'),
    #Teams.get_item(id='NCAA-UConn-W'),
]

#team_entries = Teams.scan(is_women__eq=True, league__eq='NCAA')

team_objs = {}
for tm in team_entries:
    t = TeamFactory.objectify(tm)
    team_objs[tm['id']] = t

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
s_obj = SeasonFactory.objectify(s_db)

for id in team_objs.keys():
    t = team_objs[id]
    try:
        entries = t.get_provider().get_schedule(s_obj)
        for e in entries:
            sched_entry = ScheduleEntryFactory.itemify(ScheduleEntries, id, e)
            sched_entry.save(overwrite=True)
        print "SUCCESS on %s (%i entries)" % (id, len(entries))
    except Exception as e:
        print "FAILED on %s" % id
        print e
