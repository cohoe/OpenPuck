#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Season(HawkeyApiObject):
    def __init__(self, id, league, start, end, is_women):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.league = league
        self.start_year = start
        self.end_year = end
        self.is_women = is_women
        self.short_id = '-'.join([str(start), str(end)[2:4]])

    def years(self):
        return [self.start_year, self.end_year]
