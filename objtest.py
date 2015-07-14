#!/usr/bin/env python

from hawkeyapi.providers import *

legacy_urls = [
    #'http://ritathletics.com/index.aspx?path=mhock',
    #'http://ritathletics.com/index.aspx?path=whock',
    #'http://www.rmucolonials.com/index.aspx?path=whockey',
    #'http://www.clarksonathletics.com/index.aspx?path=mhock',
]

adaptive_urls = [
    #'http://www.gonu.com/index.aspx?path=whockey',
    #'http://hurstathletics.com/index.aspx?path=whockey',
    #'http://msumavericks.com/index.aspx?path=whockey',
    #'http://cuse.com/index.aspx?path=wice',
]

cbs_urls = [
    #'http://www.gophersports.com/sports/w-hockey/minn-w-hockey-body.html',
    #'http://www.bceagles.com/sports/w-hockey/bc-w-hockey-body.html',
    #'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body.html',
    'http://www.uwbadgers.com/sports/w-hockey/wis-w-hockey-body-main.html',
]

for legacy_url in legacy_urls:
    sp = SidearmLegacyProvider(legacy_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for adaptive_url in adaptive_urls:
    sp = SidearmAdaptiveProvider(adaptive_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for cbs_url in cbs_urls:
    sp = CBSInteractiveProvider(cbs_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game
