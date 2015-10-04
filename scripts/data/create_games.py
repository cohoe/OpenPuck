#!/usr/bin/env python

from hawkeyapi.database import conn
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

try:
    games_table = Table('games', connection=conn)
    games_table.delete()
except JSONResponseError:
    print "Table 'games' does not exist."

gd_idx = GlobalAllIndex("GenderDateIndex",
                        parts=[
                            HashKey("is_women", data_type=NUMBER),
                            RangeKey("date", data_type=NUMBER),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

hl_idx = GlobalAllIndex("HomeLeagueConfIndex",
                        parts=[
                            HashKey("home_league"),
                            RangeKey("home_conference"),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

al_idx = GlobalAllIndex("AwayLeagueConfIndex",
                        parts=[
                            HashKey("away_league"),
                            RangeKey("away_conference"),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

tr_idx = GlobalAllIndex("TournamentIndex",
                        parts=[
                            HashKey("is_tournament", data_type=NUMBER),
                            RangeKey("tournament_id"),
                        ],
                        throughput={
                            'read': 1,
                            'write': 1,
                        })

tble = Table.create("games", 
                    schema=[
                        HashKey("id")
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                        gd_idx,
                        hl_idx,
                        al_idx,
                        tr_idx,
                    ],
                    connection=conn)

print "Created 'games' table"
