#!/usr/bin/env python

from hawkeyapi.providers import *

legacy_urls = [
    #'http://ritathletics.com/index.aspx?path=mhock',
    #'http://ritathletics.com/index.aspx?path=whock',
    #'http://www.rmucolonials.com/index.aspx?path=whockey',
    'http://www.clarksonathletics.com/index.aspx?path=mhock',
]

adaptive_urls = [
    'http://www.gonu.com/index.aspx?path=whockey',
    #'http://hurstathletics.com/index.aspx?path=whockey',
    #'http://msumavericks.com/index.aspx?path=whockey',
    #'http://cuse.com/index.aspx?path=wice',
]

cbs_urls = [
    #'http://www.gophersports.com/sports/w-hockey/minn-w-hockey-body.html',
    'http://www.bceagles.com/sports/w-hockey/bc-w-hockey-body.html',
    #'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body.html',
    #'http://www.uwbadgers.com/sports/w-hockey/wis-w-hockey-body-main.html',
]

pm_urls = [
    'http://www.brownbears.com/sports/w-hockey/index',
    #'http://merrimackathletics.com/sports/wice/index',
    #'http://quinnipiacbobcats.com/sports/wice/index',
    #'http://sacredheartpioneers.com/sports/w-hockey/index'
]

ps_urls = [
    'http://unhwildcats.com/sports/wice/index',
    #'http://goblackbears.com/sports/w-hockey/index',
    #'http://www.gocrimson.com/sports/wice/index',
]

pl_urls = [
    'http://www.yalebulldogs.com/sports/w-hockey/index',
]

neuc_urls = [
    'http://www.goprincetontigers.com/SportSelect.dbml?DB_OEM_ID=10600&SPID=4264&SPSID=46867&DB_OEM_ID=10600',
    #'http://www.goprincetontigers.com/SportSelect.dbml?DB_OEM_ID=10600&SPID=4275&SPSID=46915&DB_OEM_ID=10600',
]

neul_urls = [
    'http://www.dartmouthsports.com/SportSelect.dbml?&DB_OEM_ID=11600&SPID=4726&SPSID=48905',
    #'http://www.dartmouthsports.com/SportSelect.dbml?DB_OEM_ID=11600&SPID=4728&SPSID=48935&DB_OEM_ID=11600',
]

neua_urls = [
    'http://www.undsports.com/SportSelect.dbml?SPID=6405',
    #'http://www.undsports.com/SportSelect.dbml?SPID=6403',
]

strline_urls = [
    'http://www.bsubeavers.com/whockey/',
    #'http://www.bsubeavers.com/mhockey/',
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

for pm_url in pm_urls:
    sp = PrestoMonthlyProvider(pm_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for ps_url in ps_urls:
    sp = PrestoSimpleProvider(ps_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for pl_url in pl_urls:
    sp = PrestoLegacyProvider(pl_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for neuc_url in neuc_urls:
    sp = NeulionClassicProvider(neuc_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for neul_url in neul_urls:
    sp = NeulionLegacyProvider(neul_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for neua_url in neua_urls:
    sp = NeulionAdaptiveProvider(neua_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game

for strline_url in strline_urls:
    sp = StreamlineProvider(strline_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game
