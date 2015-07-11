#!/usr/bin/env python

from hawkeyapi import ScheduleParser

url = 'http://ritathletics.com/schedule.aspx?path=whock'

json_schedule = ScheduleParser.parse2json(url)
for game in json_schedule:
    print game
