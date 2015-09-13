#!/usr/bin/env python

from hawkeyapi.database import Teams, ScheduleEntries
from hawkeyapi.TestData import seasons
from hawkeyapi.objects import Team
from datetime import datetime

team_entries = [
    #Teams.get_item(id='NCAA-Harvard-W'),
    #Teams.get_item(id='NCAA-Yale-W'),
    Teams.get_item(id='NCAA-UConn-W'),
]

#team_entries = Teams.scan(is_women__eq=True, league__eq='NCAA')

team_objs = {}
for tm in team_entries:
    t = Team(
        tm['common_name'],
        tm['mascot'],
        tm['is_women'],
        tm['home_conference'],
        tm['social_media'],
        tm['web_site'],
        tm['provider'],
    )
    team_objs[tm['id']] = t

s = seasons[1]

for id in team_objs.keys():
    t = team_objs[id]
#    try:
    entries = t.get_provider().get_schedule(s)
    print len(entries)
    for e in entries:
        ScheduleEntries.put_item(data={
            'team_id': id,
            'entry_id': e.id,
            'timestamp': datetime.combine(e.date, e.start_time).isoformat(),
            'opponent': e.opponent,
            'site': e.site,
            'location': e.location,
            'is_conference_tournament': e.is_conference_tournament,
            'is_national_tournament': e.is_national_tournament,
            'links': e.links,
            'is_conference': e.is_conference,
            'season': e.season,
            'league': e.league,
        },
        overwrite=True)
    print "SUCCESS on %s" % id
#    except Exception as e:
#        print "FAILED on %s" % id
#        print e
