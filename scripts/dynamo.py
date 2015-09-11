#!/usr/bin/env python
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute
)
from datetime import datetime

class ScheduleEntryModel(Model):
    """
    A schedule entry.
    """
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "schedule_entries"
        host = "http://localhost:8000"

    team = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(range_key=True)
    id = UnicodeAttribute()
    opponent = UnicodeAttribute()
    site = UnicodeAttribute()
    location = UnicodeAttribute()
    is_conference = BooleanAttribute()
    links = JSONAttribute()
    season = UnicodeAttribute()
    league = UnicodeAttribute()


def create_table():
    if ScheduleEntryModel.exists():
        ScheduleEntryModel.delete_table()

    ScheduleEntryModel.create_table()

def add_table():
    #user_item = UserModel("Jack", "Oph")
    user_item = UserModel(first_name="Jack", last_name="Oph")
    user_item.save()

def add_entry_to_table():
    s1 = ScheduleEntryModel(
        team = "RIT WOMEN",
        timestamp = datetime.now(),
        id = "ABC12345",
        opponent = "NORTH DAKOTA",
        site = "home",
        location = "GENE POLISSENI CENTER",
        is_conference = True,
        links = "",
        season = "2014-15",
        league = "NCAA"
    )
    s1.save()
    s2 = ScheduleEntryModel(
        team = "NORTHEASTERN MEN",
        timestamp = datetime.now(),
        id = "010101",
        opponent = "NORTH DAKOTA",
        site = "home",
        location = "MATTHEWS ARENA",
        is_conference = False,
        links = "",
        season = "2014-15",
        league = "NCAA"
    )
    s2.save()


def query_table():
    #entries = ScheduleEntryModel.scan()
    entries = ScheduleEntryModel.query(site__eq='home')
    for e in entries:
        print e.dumps()

def scan_table():
    entries = ScheduleEntryModel.scan(season__eq="2014-15", league__eq="NCAA")
    for e in entries:
        print e.dumps()
    
def dump():
    content = UserModel.dumps()
    print content

if __name__ == "__main__":
    create_table()
    add_entry_to_table()
    #query_table()
    scan_table()
    #add_table()
    #query_table()
    #dump()
