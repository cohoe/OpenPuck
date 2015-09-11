#!/usr/bin/env python
from HawkeyModel import *

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
    social_media = JSONAttribute()
    website = UnicodeAttribute()
