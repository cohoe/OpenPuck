#!/usr/bin/env python
from HawkeyModel import *

class ScheduleEntryModel(HawkeyModel):
    """
    A schedule entry.
    """
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "schedule_entries"
        host = "http://localhost:8000"

    team_id = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(range_key=True)
    id = UnicodeAttribute()
    opponent = UnicodeAttribute()
    site = UnicodeAttribute()
    location = UnicodeAttribute(null=True)
    is_conference = BooleanAttribute()
    links = JSONAttribute()
    season = UnicodeAttribute()
    league = UnicodeAttribute()
    is_conference_tournament = BooleanAttribute()
    is_national_tournament = BooleanAttribute()
