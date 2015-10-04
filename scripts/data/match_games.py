#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Teams, TeamAltnames, Seasons
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory, GameFactory, TeamFactory
from boto.dynamodb2.exceptions import ItemNotFound

s_db = Seasons.get_item(id='NCAA-1415-W')
season = SeasonFactory.objectify(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
#team_id = 'NCAA-Northeastern-W'
#print "Searching for %s" % team_id
#t_entry = Teams.get_item(id=team_id)

t_entries = Teams.query_2(
    #index='ConferenceIndex',
    #home_conference__eq='HEA',
    #is_women__eq=True,
    id__eq='NCAA-BU-W',
)

for team_item in t_entries:
    team_id = team_item['id']
    team_obj = TeamFactory.objectify(team_item)

    print "Finding schedule entries..."
    entries = ScheduleEntries.query_2(
        index='TeamSeasonIndex',
        team_id__eq=team_id,
        season__eq=season.id,
    )

    # For schedule_entries for the given team...
    for e_db in entries:
        # Make an object for it
        e_obj = ScheduleEntryFactory.objectify(e_db)

        print "-----------------------------------------"
        try:
            # Find the item for the opponent
            opponent_entry = Teams.get_item(id=e_obj.opponent)
            opponent_obj = TeamFactory.objectify(opponent_entry)
            o_entry = opponent_entry
            #print "Found opponent %s" % o_entry['id']
            try:
                opponent_s_entry = ScheduleEntries.get_item(team_id=o_entry['id'], date=e_obj.date.toordinal())
                #print "Their opponent is: %s" % opponent_s_entry['opponent']
                # WE HAVE REACHED SUCCESS!!!!
                my_obj = e_obj
                their_obj = ScheduleEntryFactory.objectify(opponent_s_entry)
                #valid_status = GameFactory.construct(my_obj, their_obj)
                game_obj = GameFactory.construct2(team_obj, my_obj, opponent_obj, their_obj)
                if valid_status is True:
                    print "PASSED: '%s vs %s'" % (my_obj.team_id, their_obj.team_id)
                else:
                    print "FAILED: '%s' vs '%s' on '%s'" % (my_obj.team_id, their_obj.team_id, my_obj.date)
            except Exception as e:
                print "Could not find matching schedule entry (%s)" % e
                #pass
        except ItemNotFound:
            print "Could not find opponent %s" % e_obj.opponent
        except Exception as e:
            print "Failed to find %s" % e_obj.opponent
            print e
        print "-----------------------------------------\n"
