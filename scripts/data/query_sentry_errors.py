#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Seasons
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory
from datetime import date

s_db = Seasons.get_item(id='NCAA-1415-W')
season = SeasonFactory.objectify(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
#entries = ScheduleEntries.query_2(
#    team_id__eq='NCAA-Yale-W'
#)

start_date = date(2014, 9, 20).toordinal()
end_date = date(2015, 4, 30).toordinal()

entries = ScheduleEntries.scan(
    #team_id__eq='NCAA-Yale-W',
    #index='LeagueDateIndex',
    league__eq='NCAA',
    date__between=[start_date, end_date],
    normal_loc__eq=False,
)

for e_db in entries:
    print "--------------------------------"
    print "Entry Team: '%s'" % e_db['team_id']
    print "Opponent:   '%s'" % e_db['opponent']
    print "Location:   '%s'" % e_db['location']
    print "--------------------------------\n"
