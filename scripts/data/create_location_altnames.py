#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex, AllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    altnames_table = Table('location_altnames', connection=conn)
    altnames_table.delete()
except JSONResponseError:
    print "Table 'location_altnames' does not exist."

al_idx = GlobalAllIndex("AltnameIndex",
                        parts=[
                            HashKey("affiliation"),
                            RangeKey("altname"),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

altnames_table = Table.create("location_altnames", 
                            schema=[
                                HashKey("location_id"),
                                RangeKey("altname"),
                            ],
                            throughput={
                                'read': 1,
                                'write': 1
                            },
                            global_indexes=[
                                al_idx
                            ],
                            indexes=[
                            ],
                            connection=conn)

print "Created 'location_altnames' table"
