#!/usr/bin/env python

from hawkeyapi.models import TeamModel
from hawkeyapi.objects import Team
from hawkeyapi.TestData import seasons


s = seasons[1]

#teams = TeamModel.scan()
teams = TeamModel.conference_index.query('CHA', is_women__eq=True)

for e in teams:
    t = Team(
        e.name,
        e.mascot,
        e.is_women,
        e.home_conference,
        e.social_media,
        e.web_site,
        e.web_provider,
    )

    print ""
    print "%s - %s" % (t.institution_name, s.id)

    team_provider = t.get_provider()

    try:
        sched_entries = team_provider.get_schedule(s)
        print "%s Parsed %i entries" % (t.provider, len(sched_entries))
    except Exception as e:
        print "FAILED"
        print "  Specific error: %s" % e
        continue

    print "SUCCESS"
