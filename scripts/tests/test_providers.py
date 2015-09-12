#!/usr/bin/env python

from hawkeyapi.models import TeamModel
from hawkeyapi.objects import Team
from hawkeyapi.TestData import seasons


s = seasons[1]

teams = TeamModel.scan(is_women__eq=True)
#teams = TeamModel.conference_index.query('Independent', is_women__eq=True)
#teams = TeamModel.conference_index.query('ECAC', is_women__eq=True, name__begins_with='Clarkson')

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

#    sched_entries = team_provider.get_schedule(s)
#    print "%s Parsed %i entries" % (t.provider, len(sched_entries))

    try:
        sched_entries = team_provider.get_schedule(s)
        print "%s Parsed %i entries" % (t.provider, len(sched_entries))
    except Exception as e:
        print "FAILED"
        print "  Specific error: %s" % e
        continue

    print "SUCCESS"
