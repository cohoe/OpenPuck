#!/usr/bin/env python

from hawkeyapi.objects import Season, Team

# Define the provider and URLs to test
PROVIDER = 'PrestoSimpleProvider'
TEST_URLS = [
    'http://www.gocrimson.com/sports/wice/index',
]

# Create a fake season object to hand to the provider for data
seasonObj = Season(
    id='abcdefghijk',
    league='NCDoubleDollar',
    start=2016,
    end=2017,
    is_women=True
)

# Create a team object for each URL that we were given
teams = []
for url in TEST_URLS:
    teamObj = Team(
        id='lolzwatteam',
        institution='Doesnt Matter',
        mascot='lolcats',
        is_women=True,
        home_conference='LOLZWHATISTHIS',
        social_media='FOOBAR',
        web_site=url,
        web_provider=PROVIDER,
        league='LOLZLEAGUE'
    )
    teams.append(teamObj)

# For each team print their schedule
for teamObj in teams:
    print "%s :: %s" % (teamObj.provider, teamObj.website)
    scheduleList = teamObj.get_provider().get_schedule(seasonObj)
    for game in scheduleList:
        print game

    print "Total: %d" % len(scheduleList)
