#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex, AllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    schedule_entries_table = Table('schedule_entries', connection=conn)
    schedule_entries_table.delete()
except JSONResponseError:
    print "Table 'schedule_entries' does not exist."

#teams_conference_index = GlobalAllIndex("Conference-Id-Index",
#                                        parts=[
#                                            HashKey("home_conference"),
#                                            RangeKey("is_women", data_type=NUMBER),
#                                        ],
#                                        throughput={
#                                            'read': 1,
#                                            'write': 1
#                                        })

schedule_entries_table = Table.create("schedule_entries", 
                            schema=[
                                HashKey("team_id"),
                                RangeKey("timestamp"),
                            ],
                            throughput={
                                'read': 1,
                                'write': 1
                            },
                            indexes=[
                                sentries_teamid_index,
                            ],
                            connection=conn)

print "Created 'schedule_entries' table"