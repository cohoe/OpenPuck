#!/usr/bin/env python

from hawkeyapi.database import Teams

Teams.put_item(data={
    'id': 'NCAA-RIT-W',
    'institution': 'Rochester Institute of Technology',
    'mascot': 'Tigers',
})

#item = Teams.get_item('NCAA-RIT-W')
#print item['id']
