#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries, Seasons, TeamAltnames
from hawkeyapi.factories import TeamFactory, SeasonFactory, ScheduleEntryFactory

team_entries = [
    Teams.get_item(id='NCAA-Harvard-W'),
    Teams.get_item(id='NCAA-Yale-W'),
    #Teams.get_item(id='NCAA-UConn-W'),
]

#team_entries = Teams.scan(is_women__eq=True, league__eq='NCAA')

s_db = Seasons.get_item(id='NCAA-1415-W')
s_obj = SeasonFactory.objectify(s_db)

for t_db in team_entries:
    t_obj = TeamFactory.objectify(t_db)

    try:
        entries = t_obj.get_provider().get_schedule(s_obj)
        for e in entries:
            try:
                opponent_team_items = TeamAltnames.query_2(
                    index='AltnamesGenderIndex',
                    altname__eq=e.opponent,
                    is_women__eq=e.is_women,
                )
                # Really need a helper function for this.
                results_list = list(opponent_team_items)
                num_results = len(results_list)
                if num_results == 0:
                    raise Exception("No opponent altname found (%s)" % e.opponent)
                elif num_results > 1:
                    raise Exception("Too many opponent altnames found (%s)" % e.opponent)
                else:
                    e.opponent = results_list[0]['team_id']
            except Exception as ex:
                print ex
            sched_entry = ScheduleEntryFactory.itemify(ScheduleEntries, e)
            sched_entry.save(overwrite=True)
        print "SUCCESS on %s (%i entries)" % (t_obj.id, len(entries))
    except Exception as e:
        print "FAILED on %s" % t_obj.id
        print e
