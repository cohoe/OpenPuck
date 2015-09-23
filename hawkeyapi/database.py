#!/usr/bin/env python

from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection

conn = DynamoDBConnection(host='localhost', port=8000,
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy',
    is_secure=False,
)

Teams = Table('teams', connection=conn)
ScheduleEntries = Table('schedule_entries', connection=conn)
TeamAltnames = Table('team_altnames', connection=conn)
Seasons = Table('seasons', connection=conn)
SeasonPhases = Table('season_phases', connection=conn)
