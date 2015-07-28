#!/usr/bin/env python

from hawkeyapi.providers import *
from hawkeyapi.util import *
from hawkeyapi.objects import ScheduleEntry, Season, Team, Conference, Institution

s1 = Season(
    "NCAA",
    True,
    2013,
    2014,
    ("2013-09-25", "2014-02-23"),
    ("2014-02-28", "2014-03-09"),
    ("2014-03-10", "2014-03-23")
)
s2 = Season(
    "NCAA",
    True,
    2014,
    2015,
    ("2014-10-03", "2015-02-20"),
    ("2015-02-27", "2015-03-08"),
    ("2015-03-13", "2015-03-25")
)
s3 = Season(
    "NCAA",
    True,
    2015,
    2016,
    ("2015-09-24", "2016-02-21"),
    ("2016-02-26", "2016-03-06"),
    ("2016-03-11", "2016-03-20")
)

seasons = [s1, s2, s3]

t = Team(
    "Rochester Institute of Technology",
    "Tigers",
    True,
    "College Hockey America",
    {'twitter': '@RITWHKY', 'instagram': '@ritwhky'},
    {'index_url': 'http://ritathletics.com/index.aspx?path=whock', 'data_provider': 'SidearmLegacyProvider'},
)

print t.json()
for s in seasons:
    p = t.get_provider()
    entries = p.get_schedule(s)
    for e in entries:
        print e.json()
        exit(1)
