#!/usr/bin/env python

from hawkeyapi.models import TeamModel

t = TeamModel.get('NCAA-RIT-W')

t.altnames = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']

t.save()

#t_query = TeamModel.scan(altnames__contains='RIT')
#t_query = TeamModel.conference_index.query('AHC', altnames__contains='RIT')
t_query = TeamModel.query('NCAA-RIT-W', altnames__contains="RIT")

for result in t_query:
    print result.id
