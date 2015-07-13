#!/usr/bin/env python

from hawkeyapi.providers import *

#url = 'http://ritathletics.com/schedule.aspx?path=whock'
#index_url = 'http://ritathletics.com/index.aspx?path=mhock'
#index_url = 'http://ritathletics.com/index.aspx?path=whock'
#index_url = 'http://www.rmucolonials.com/index.aspx?path=whockey'
#index_url = 'http://www.clarksonathletics.com/index.aspx?path=mhock'

index_urls = [
    #'http://www.gonu.com/index.aspx?path=whockey',
    #'http://hurstathletics.com/index.aspx?path=whockey',
    'http://msumavericks.com/index.aspx?path=whockey',
]

for index_url in index_urls:
    sp = SidearmAdaptiveProvider(index_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game
