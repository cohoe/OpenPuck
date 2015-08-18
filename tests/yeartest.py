#!/usr/bin/env python

from hawkeyapi.providers import *
from hawkeyapi.util import *
from hawkeyapi.objects import ScheduleEntry, Season, Team, Conference, Institution

from hawkeyapi.TestData import seasons, teams

teams = teams[0:]
seasons = seasons[0:]

for i, t in enumerate(teams):
#for t in teams:
    #print t.json()
    #for s in seasons:
    for k, s in enumerate(seasons):
        #print "T:%i, S:%i" % (i, k)
        print ""
        print t.institution_name
        print s.id
        #print s.json()
        p = t.get_provider()
        try:
            entries = p.get_schedule(s)
            for e in entries:
                #print e
                print e.opponent
        except requests.HTTPError:
            print "***** Season %s not available *****" % s.id
