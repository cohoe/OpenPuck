#!/usr/bin/env python

from datetime import datetime
from hawkeyapi.models import ScheduleEntryModel, TeamModel
from hawkeyapi.objects import Team
from hawkeyapi.TestData import seasons

team_models = [
    TeamModel.get('NCAA-Harvard-W'),
    TeamModel.get('NCAA-Yale-W'),
]

teams = {}
for tm in team_models:
    t = Team(
        tm.common_name,
        tm.mascot,
        tm.is_women,
        tm.home_conference,
        tm.social_media,
        tm.web_site,
        tm.web_provider,
    )
    teams[tm.id] = t

s = seasons[1]

for id in teams.keys():
    t = teams[id]
    entries = t.get_provider().get_schedule(s)
    print id
    for e in entries:
        sem = ScheduleEntryModel(
            team_id = id,
            id = e.id,
            timestamp = datetime.combine(e.date, e.start_time),
            opponent = e.opponent,
            site = e.site,
            location = e.location,
            is_conference_tournament = e.is_conference_tournament,
            is_national_tournament = e.is_national_tournament,
            links = e.links,
            is_conference = e.is_conference,
            season = e.season,
            league = e.league,
        )
        sem.save()
