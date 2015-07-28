#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Season(HawkeyApiObject):
    def __init__(self, league, is_women, start, end, confplay=None, conftour=None, nattour=None):
        HawkeyApiObject.__init__(self)

        self.id = '-'.join([str(start), str(end)[2:4]])
        self.start_year = start
        self.end_year = end
        self.league = league

        self.phases = {
            'ConferencePlay': confplay,
            'ConferenceTournament': conftour,
            'NationalTournament': nattour,
        }


    def years(self):
        return [self.start_year, self.end_year]
