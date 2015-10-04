#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    locations_table = Table('locations', connection=conn)
    locations_table.delete()
except JSONResponseError:
    print "Table 'locations' does not exist."

st_idx = GlobalAllIndex("StateIndex",
                        parts=[
                            HashKey("state"),
                            RangeKey("city"),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })


tble = Table.create("locations", 
                    schema=[
                        HashKey("id")
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                        st_idx,
                    ],
                    connection=conn)

print "Created 'locations' table"
