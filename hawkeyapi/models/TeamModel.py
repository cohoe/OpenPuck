#!/usr/bin/env python
from HawkeyModel import *

class ConferenceIndex(GlobalSecondaryIndex):
    """
    Index for viewing teams by conference
    """
    class Meta:
        index_name = 'team_conference_index'
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()
    
    home_conference = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    is_women = BooleanAttribute()

class TeamModel(HawkeyModel):
    """
    Model for a team.
    """
    class Meta:
        table_name = "teams"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    name = UnicodeAttribute(hash_key=True)
    is_women = BooleanAttribute(range_key=True)
    mascot = UnicodeAttribute()
    home_conference = UnicodeAttribute()
    social_media = JSONAttribute(default="")
    web_site = UnicodeAttribute()
    web_provider = UnicodeAttribute()
    league = UnicodeAttribute()
    conference_index = ConferenceIndex()
