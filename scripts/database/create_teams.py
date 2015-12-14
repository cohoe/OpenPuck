#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    teams_table = Table('teams', connection=conn)
    teams_table.delete()
except JSONResponseError:
    print "Table 'teams' does not exist."

pr_idx = GlobalAllIndex("ProviderIndex",
                        parts=[
                            HashKey("provider"),
                            RangeKey("is_women", data_type=NUMBER),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

co_idx = GlobalAllIndex("ConferenceIndex",
                        parts=[
                            HashKey("home_conference"),
                            RangeKey("is_women", data_type=NUMBER),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

tble = Table.create("teams", 
                    schema=[
                        HashKey("id")
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                        co_idx,
                        pr_idx,
                    ],
                    connection=conn)

print "Created 'teams' table"
