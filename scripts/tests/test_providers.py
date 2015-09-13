#!/usr/bin/env python

import traceback
from hawkeyapi.factories import SeasonFactory, TeamFactory
from hawkeyapi.database import Teams, Seasons

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
season = SeasonFactory.make(s_db)

teams = Teams.scan(is_women__eq=True)
#teams = TeamModel.conference_index.query('Independent', is_women__eq=False)
#teams = TeamModel.conference_index.query('NCHC', is_women__eq=False, name__begins_with='University of Nebraska')

for e in teams:
    try:
        t = TeamFactory.make(e)
        team_provider = t.get_provider()
    except Exception as ex:
        print "Totally blew up on %s" % e['id']
        print "  Specific error: %s" % ex
        print(traceback.format_exc())
        continue

    print ""
    print "%s - %s" % (t.institution_name, season.id)


#    sched_entries = team_provider.get_schedule(s)
#    print "%s Parsed %i entries" % (t.provider, len(sched_entries))


    try:
        sched_entries = team_provider.get_schedule(season)
        print "%s Parsed %i entries" % (t.provider, len(sched_entries))
    except Exception as e:
        print "FAILED"
        print "  Specific error: %s" % e
        continue

    print "SUCCESS"
