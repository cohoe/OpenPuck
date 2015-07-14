#!/usr/bin/env python

from hawkeyapi.providers import *

legacy_urls = [
    #'http://ritathletics.com/index.aspx?path=mhock'
    'http://ritathletics.com/index.aspx?path=whock'
    #'http://www.rmucolonials.com/index.aspx?path=whockey'
    #'http://www.clarksonathletics.com/index.aspx?path=mhock'
]

index_urls = [
    'http://www.gonu.com/index.aspx?path=whockey',
    #'http://hurstathletics.com/index.aspx?path=whockey',
    #'http://msumavericks.com/index.aspx?path=whockey',
    #'http://cuse.com/index.aspx?path=wice',
]

for index_url in legacy_urls:
    #sp = SidearmAdaptiveProvider(index_url)
    sp = SidearmLegacyProvider(index_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game
