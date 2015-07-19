#!/usr/bin/env python

from hawkeyapi.providers import *
from hawkeyapi.objects import ScheduleEntry, Season

s = Season(
    2014,
    2015,
    ("2015-09-24", "2016-02-21"),
    ("2016-02-26", "2016-03-06"),
    ("2016-03-11", "2016-03-20")
)

print s.json()
