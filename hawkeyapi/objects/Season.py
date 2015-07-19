#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Season(HawkeyApiObject):
    def __init__(self, start, end, confplay=None, conftour=None, nattour=None):
        HawkeyApiObject.__init__(self)

        self.id = '-'.join([str(start), str(end)[2:4]])
        self.start_year = start
        self.end_year = end

        self.phases = {
            'ConferencePlay': confplay,
            'ConferenceTournament': conftour,
            'NationalTournament': nattour,
        }
