#!/usr/bin/env python

from hawkeyapi.providers import *
from hawkeyapi.util import *
from hawkeyapi.objects import ScheduleEntry, Season, Team, Conference, Institution

from hawkeyapi.TestData import seasons, teams

teams = teams[5:]
seasons = seasons[0:]

for t in teams:
    print t.json()
    for s in seasons:
        print s.json()
        p = t.get_provider()
        entries = p.get_schedule(s)
        for e in entries:
            print e
