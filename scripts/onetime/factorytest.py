#!/usr/bin/env python

from hawkeyapi.factories import SeasonFactory
from hawkeyapi.database import Seasons

season = Seasons.get_item(league='NCAA', id='2014-15W')

s_obj = SeasonFactory.objectify(season)
s_item = SeasonFactory.itemify(Seasons, s_obj)
s_item.save(overwrite=True)
