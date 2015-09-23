#!/usr/bin/env python

from hawkeyapi.database import Seasons
from hawkeyapi.factories import SeasonFactory

s_db = Seasons.get_item(id='NCAA-1415-W')
s_obj = SeasonFactory.objectify(s_db)

print s_obj.json()
