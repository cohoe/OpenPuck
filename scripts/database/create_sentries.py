#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex, AllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER, STRING

try:
    schedule_entries_table = Table('schedule_entries', connection=conn)
    schedule_entries_table.delete()
except JSONResponseError:
    print "Table 'schedule_entries' does not exist."

ld_idx = GlobalAllIndex("LeagueDateIndex",
                        parts=[
                            HashKey("league", data_type=STRING),
                            RangeKey("date", data_type=NUMBER),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

team_idx = AllIndex("TeamSeasonIndex",
                    parts=[
                        HashKey("team_id"),
                        RangeKey("season"),
                    ])

tble = Table.create("schedule_entries",
                    schema=[
                        HashKey("team_id"),
                        RangeKey("date", data_type=NUMBER),
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                        ld_idx
                    ],
                    indexes=[
                        team_idx
                    ],
                    connection=conn)

print "Created 'schedule_entries' table"
