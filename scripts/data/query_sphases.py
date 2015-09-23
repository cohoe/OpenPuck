#!/usr/bin/env python

from hawkeyapi.database import SeasonPhases
from hawkeyapi.factories import SeasonPhaseFactory
from datetime import date

s_db = SeasonPhases.get_item(id='NCAA-1415-W', name='ConferencePlay')
s_obj = SeasonPhaseFactory.objectify(s_db)

print s_obj.json()
