#!/usr/bin/env python

from hawkeyapi.database import Teams

b_team = Teams.get_item(id='NCAA-RIT-W')
b_team['altnames'] = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']
b_team.save()

b_query = Teams.scan(altnames__contains='RIT')
for result in b_query:
    print result['id']
