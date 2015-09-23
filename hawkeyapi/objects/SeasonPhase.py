#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class SeasonPhase(HawkeyApiObject):
    def __init__(self, id, name, start, end):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.name = name
        self.start = start
        self.end = end
