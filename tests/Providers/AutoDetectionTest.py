#!/usr/bin/env python

from hawkeyapi.objects import Season, Team
from hawkeyapi.providers import get_provider_for_url

seasonObj = Season(
    id='abcdefghijk',
    league='NCDoubleDollar',
    start=2016,
    end=2017,
    is_women=True
)

testData = [
    {'provider': 'CBSInteractiveProvider', 'url': 'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body-main.html'},
    {'provider': 'NeulionAdaptiveProvider', 'url': 'http://www.undsports.com/SportSelect.dbml?spid=6403'},
    {'provider': 'NeulionClassicProvider', 'url': 'http://www.omavs.com/SportSelect.dbml?&DB_OEM_ID=31400&SPID=135111&SPSID=795013'},
    {'provider': 'NeulionLegacyProvider', 'url': 'http://www.gogriffs.com/SportSelect.dbml?SPID=12001'},
    {'provider': 'PrestoLegacyProvider', 'url': 'http://www.yalebulldogs.com/sports/w-hockey/index'},
    {'provider': 'PrestoMonthlyProvider', 'url': 'http://www.brownbears.com/sports/w-hockey/index'},
    {'provider': 'PrestoSimpleProvider', 'url': 'http://www.gocrimson.com/sports/wice/index'},
    {'provider': 'SidearmAdaptiveProvider', 'url': 'http://ritathletics.com/index.aspx?path=whock'},
    {'provider': 'SidearmLegacyProvider', 'url': 'http://www.clarksonathletics.com/index.aspx?path=whock'},
    {'provider': 'SidearmResponsiveProvider', 'url': 'http://goprincetontigers.com/index.aspx?path=whockey'},
    {'provider': 'StreamlineProvider', 'url': 'http://www.bsubeavers.com/whockey/'},
    {'provider': 'NWHLProvider', 'url': 'https://nwhl.zone/'}
]

for item in testData:
    print "---------"
    print "URL: %s" % item['url']
    print "    The real provider is: %s" % item['provider']
    provider = get_provider_for_url(item['url'])
    if provider is not None:
        print "The detected provider is: %s" % provider.get_name()
    else:
        print "No provider detected!"

    print "---------"
