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

#item = Teams.get_item('NCAA-RIT-W')
#print item['id']
