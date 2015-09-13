#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    altnames_table = Table('team_altnames', connection=conn)
    altnames_table.delete()
except JSONResponseError:
    print "Table 'team_altnames' does not exist."

altnames_gender_index = GlobalAllIndex("AltnamesGenderIndex",
                                       parts=[
                                           HashKey("altname"),
                                           RangeKey("is_women", data_type=NUMBER),
                                       ],
                                       throughput={
                                           'read': 1,
                                           'write': 1
                                       })

altnames_table = Table.create("team_altnames", 
                            schema=[
                                HashKey("team_id"),
                                RangeKey("altname"),
                            ],
                            throughput={
                                'read': 1,
                                'write': 1
                            },
                            global_indexes=[
                                altnames_gender_index,
                            ],
                            connection=conn)

print "Created 'team_altnames' table"
