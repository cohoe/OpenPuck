#!/usr/bin/env python

from hawkeyapi.objects import Season, Team

seasonObj = Season(
    id='abcdefghijk',
    league='NCDoubleDollar',
    start=2016,
    end=2017,
    is_women=True
)

# NeulionClassic might have been killed
testData = [
#    {'provider': 'SidearmLegacyProvider', 'url': 'http://www.clarksonathletics.com/index.aspx?path=whock'},
#    {'provider': 'SidearmAdaptiveProvider', 'url': 'http://ritathletics.com/index.aspx?path=whock'},
#    {'provider': 'NeulionLegacyProvider', 'url': 'http://www.omavs.com/SportSelect.dbml?&DB_OEM_ID=31400&SPID=135111&SPSID=795013'},
#    {'provider': 'NeulionAdaptiveProvider', 'url': 'http://www.undsports.com/SportSelect.dbml?spid=6403'},
#    {'provider': 'PrestoMonthlyProvider', 'url': 'http://www.brownbears.com/sports/w-hockey/index'},
#    {'provider': 'PrestoLegacyProvider', 'url': 'http://www.yalebulldogs.com/sports/w-hockey/index'},
#    {'provider': 'PrestoSimpleProvider', 'url': 'http://www.gocrimson.com/sports/wice/index'},
#    {'provider': 'CBSInteractiveProvider', 'url': 'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body-main.html'},
#    {'provider': 'StreamlineProvider', 'url': 'http://www.bsubeavers.com/whockey/'}
]

teams = []
for test in testData:
    teamObj = Team(
        id='lolzwatteam',
        institution='Doesnt Matter',
        mascot='lolcats',
        is_women=True,
        home_conference='LOLZWHATISTHIS',
        social_media='FOOBAR',
        web_site=test['url'],
        web_provider=test['provider'],
        league='LOLZLEAGUE'
    )
    teams.append(teamObj)

for teamObj in teams:
    print teamObj
    print "%s :: %s" % (teamObj.provider, teamObj.website)
    scheduleList = teamObj.get_provider().get_schedule(seasonObj)
    for game in scheduleList:
        print game
