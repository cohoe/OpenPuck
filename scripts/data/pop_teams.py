#!/usr/bin/env python

from hawkeyapi.database import Teams

Teams.put_item(data={
    'id': 'NCAA-RIT-W',
    'institution': 'Rochester Institute of Technology',
    'mascot': 'Tigers',
    'home_conference': 'CHA',
    'is_women': True,
    'league': 'NCAA',
    'provider': 'SidearmLegacyProvider',
    'website': 'http://ritathletics.com/index.aspx?path=whock',
}, overwrite=True)

Teams.put_item(data={
    'id': 'NCAA-Harvard-W',
    'institution': 'Harvard University',
    'mascot': 'Crimson',
    'home_conference': 'ECAC',
    'is_women': True,
    'league': 'NCAA',
    'provider': 'PrestoSimpleProvider',
    'website': 'http://www.gocrimson.com/sports/wice/index',
}, overwrite=True)

Teams.put_item(data={
    'id': 'NCAA-Yale-W',
    'institution': 'Yale University',
    'mascot': 'Bulldogs',
    'home_conference': 'ECAC',
    'is_women': True,
    'league': 'NCAA',
    'provider': 'PrestoLegacyProvider',
    'website': 'http://www.yalebulldogs.com/sports/w-hockey/index',
}, overwrite=True)

#item = Teams.get_item('NCAA-RIT-W')
#print item['id']
