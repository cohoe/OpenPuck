#!/usr/bin/env python

from hawkeyapi.database import Locations, LocationAltnames, Teams
from hawkeyapi.factories import TeamFactory, LocationFactory
from boto.dynamodb2.exceptions import ItemNotFound
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--id", dest='location_id', required=True)
parser.add_argument("--affiliation", dest='team_id', required=True)
parser.add_argument("altname", metavar="ALTNAME")

args = parser.parse_args()

location_id = args.location_id
team_id = args.team_id
new_altname = args.altname

try:
    t_db = Teams.get_item(id=team_id)
    t_obj = TeamFactory.objectify(t_db)
except ItemNotFound as inf:
    print "ERROR: Team '%s' not found." % team_id
    exit(1)

try:
    l_db = Locations.get_item(id=location_id)
    l_obj = LocationFactory.objectify(l_db)
except ItemNotFound as inf:
    print "ERROR: location '%s' not found." % location_id
    exit(1)

LocationAltnames.put_item(data={
    'location_id': location_id,
    'affiliation': team_id,
    'altname': new_altname,
},
overwrite=True)

alts = LocationAltnames.query_2(location_id__eq=location_id)
print "SUCCESS: " + str([t['altname'] for t in alts])
