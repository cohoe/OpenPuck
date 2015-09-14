#!/usr/bin/env python

from hawkeyapi.database import Teams, TeamAltnames
from hawkeyapi.factories import TeamFactory
from boto.dynamodb2.exceptions import ItemNotFound
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--id", dest='team_id', required=True)
parser.add_argument("altname", metavar="ALTNAME")

args = parser.parse_args()

team_id = args.team_id
new_altname = args.altname

#team_id = 'NCAA-Harvard-W'
#new_altname = 'HARVARD'

try:
    t_db = Teams.get_item(id=team_id)
    t_obj = TeamFactory.make(t_db)
except ItemNotFound as inf:
    print "ERROR: Team '%s' not found." % team_id
    exit(1)

TeamAltnames.put_item(data={
    'team_id': team_id,
    'altname': new_altname,
    'is_women': t_obj.is_women,
    'league': t_obj.league,
},
overwrite=True)

alts = TeamAltnames.query_2(team_id__eq=team_id)
print "SUCCESS: " + str([t['altname'] for t in alts])
