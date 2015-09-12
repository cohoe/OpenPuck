#!/usr/bin/env python

from hawkeyapi.models import TeamModel

t = TeamModel.get('NCAA-RIT-M')
t.altnames = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']
t.save()

from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection
con = DynamoDBConnection(host='localhost', port=8000,
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy',
    is_secure=False,
)
teams = Table('teams', connection=con)

b_team = teams.get_item(id='NCAA-RIT-W')
b_team['altnames'] = ['RIT', 'ROCHESTER INSTITUTE OF TECHNOLOGY', 'ROCHESTER INST OF TECHNOLOGY']
b_team.save()

b_query = teams.scan(altnames__contains='RIT')
#print len(list(b_query))
for result in b_query:
    print "hi"
    print result['id']

#t_query = TeamModel.scan(altnames__contains='RIT')
#t_query = TeamModel.conference_index.query('AHC', altnames__contains='RIT')

#_query = TeamModel.query('NCAA-RIT-W', altnames__contains="RIT")

#for result in t_query:
#   print result.id
