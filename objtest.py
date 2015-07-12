#!/usr/bin/env python

from hawkeyapi.providers import *

#url = 'http://ritathletics.com/schedule.aspx?path=whock'
#index_url = 'http://ritathletics.com/index.aspx?path=mhock'
index_url = 'http://ritathletics.com/index.aspx?path=whock'
#index_url = 'http://www.rmucolonials.com/index.aspx?path=whockey'
#index_url = 'http://www.clarksonathletics.com/index.aspx?path=whock'

sp = SidearmLegacyProvider(index_url)

print sp.urls['schedule']
#sp.urls['schedule'] = "http://ritathletics.com/schedule.aspx?schedule=324&path=whock"
games = sp.get_schedule()
for game in games:
    print game

