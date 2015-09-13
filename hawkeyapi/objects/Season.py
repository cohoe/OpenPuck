#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Season(HawkeyApiObject):
    def __init__(self, league, id, is_women, start, end, confplay=None, conftour=None, nattour=None):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.start_year = start
        self.end_year = end
        self.league = league
        self.is_women = is_women
        self.short_id = '-'.join([str(start), str(end)[2:4]])

        self.phases = {
            'ConferencePlay': confplay,
            'ConferenceTournament': conftour,
            'NationalTournament': nattour,
        }


    def years(self):
        return [self.start_year, self.end_year]
