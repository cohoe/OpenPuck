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
    id = UnicodeAttribute(range_key=True)
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

    id = UnicodeAttribute(hash_key=True)
    institution = UnicodeAttribute()
    common_name = UnicodeAttribute()
    is_women = BooleanAttribute()
    mascot = UnicodeAttribute(null=True)
    home_conference = UnicodeAttribute()
    social_media = JSONAttribute(null=True)
    web_site = UnicodeAttribute(null=True)
    web_provider = UnicodeAttribute()
    league = UnicodeAttribute()
    conference_index = ConferenceIndex()
