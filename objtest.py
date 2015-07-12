#!/usr/bin/env python

from hawkeyapi.providers import *

#url = 'http://ritathletics.com/schedule.aspx?path=whock'
index_url = 'http://ritathletics.com/index.aspx?path=whock'

sp = SidearmLegacyProvider(index_url)

print sp.urls['schedule']
games = sp.get_schedule()
for game in games:
    print game

