#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    seasons_table = Table('seasons', connection=conn)
    seasons_table.delete()
except JSONResponseError:
    print "Table 'seasons' does not exist."

seasons_table = Table.create("seasons", 
                            schema=[
                                HashKey("id"),
                            ],
                            throughput={
                                'read': 1,
                                'write': 1
                            },
                            global_indexes=[
                            ],
                            connection=conn)

print "Created 'seasons' table"
