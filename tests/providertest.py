#!/usr/bin/env python

from hawkeyapi.objects import Season, Team
import hawkeyapi.providers
from hawkeyapi.util import get_html_from_url, get_soup_from_content
import inspect
import re

seasonObj = Season(
    id='abcdefghijk',
    league='NCDoubleDollar',
    start=2016,
    end=2017,
    is_women=True
)

# @TODO: Streamline.
testData = [
    # {'provider': 'CBSInteractiveProvider', 'url': 'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body-main.html'},
    # {'provider': 'NeulionAdaptiveProvider', 'url': 'http://www.undsports.com/SportSelect.dbml?spid=6403'},
    # {'provider': 'NeulionClassicProvider', 'url': 'http://www.omavs.com/SportSelect.dbml?&DB_OEM_ID=31400&SPID=135111&SPSID=795013'},
    # {'provider': 'NeulionLegacyProvider', 'url': 'http://www.gogriffs.com/SportSelect.dbml?SPID=12001'},
    # {'provider': 'PrestoLegacyProvider', 'url': 'http://www.yalebulldogs.com/sports/w-hockey/index'},
    # {'provider': 'PrestoMonthlyProvider', 'url': 'http://www.brownbears.com/sports/w-hockey/index'},
    # {'provider': 'PrestoSimpleProvider', 'url': 'http://www.gocrimson.com/sports/wice/index'},
    # {'provider': 'SidearmAdaptiveProvider', 'url': 'http://ritathletics.com/index.aspx?path=whock'},
    # {'provider': 'SidearmLegacyProvider', 'url': 'http://www.clarksonathletics.com/index.aspx?path=whock'},
    # {'provider': 'SidearmResponsiveProvider', 'url': 'http://goprincetontigers.com/index.aspx?path=whockey'},
    {'provider': 'StreamlineProvider', 'url': 'http://www.bsubeavers.com/whockey/'}
]

def get_list_of_providers():
    providers = []
    for name, obj in inspect.getmembers(hawkeyapi.providers):
        if inspect.isclass(obj):
            providers.append(obj)

    return providers

def get_provider_name(provider):
    name = str(provider).split('.')[-1]
    return name.replace("'>", "")

for item in testData:
    print "---------"
    print "URL: %s" % item['url']
    print "    The real provider is: %s" % item['provider']

    site_content = get_soup_from_content(get_html_from_url(item['url']))
    for provider in get_list_of_providers():
        # print "%s said %s" % (get_provider_name(provider), provider.detect(site_content))
        if provider.detect(site_content) is True:
            print "The detected provider is: %s" % get_provider_name(provider)

    print "---------"
