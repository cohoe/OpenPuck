#!/usr/bin/env python

from hawkeyapi.providers import *

#url = 'http://ritathletics.com/schedule.aspx?path=whock'
#index_url = 'http://ritathletics.com/index.aspx?path=mhock'
#index_url = 'http://ritathletics.com/index.aspx?path=whock'
#index_url = 'http://www.rmucolonials.com/index.aspx?path=whockey'
#index_url = 'http://www.clarksonathletics.com/index.aspx?path=mhock'

index_urls = []
index_urls.append('http://ritathletics.com/index.aspx?path=whock')
index_urls.append('http://ritathletics.com/index.aspx?path=mhock')
index_urls.append('http://www.rmucolonials.com/index.aspx?path=whockey')
index_urls.append('http://www.rmucolonials.com/index.aspx?path=mhockey')
index_urls.append('http://www.clarksonathletics.com/index.aspx?path=whock')
index_urls.append('http://www.clarksonathletics.com/index.aspx?path=mhock')

for index_url in index_urls:
    sp = SidearmLegacyProvider(index_url)

    print sp.urls['schedule']
    games = sp.get_schedule()
    for game in games:
        print game
