#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    seasons_table = Table('season_phases', connection=conn)
    seasons_table.delete()
except JSONResponseError:
    print "Table 'season_phases' does not exist."

seasons_table = Table.create("season_phases", 
                            schema=[
                                HashKey("id"),
                                RangeKey("name"),
                            ],
                            throughput={
                                'read': 1,
                                'write': 1
                            },
                            global_indexes=[
                            ],
                            connection=conn)

print "Created 'season_phases' table"
