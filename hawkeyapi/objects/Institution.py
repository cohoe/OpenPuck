#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Institution(HawkeyApiObject):
    def __init__(self, name, abbreviation, address=None):
        HawkeyApiObject.__init__(self)

        self.name = name
        self.abbreviation = abbreviation
        self.address = address
