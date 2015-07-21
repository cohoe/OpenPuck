#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Conference(HawkeyApiObject):
    def __init__(self, name, abbreviation, association, division, is_women, members):
        HawkeyApiObject.__init__(self)

        self.name = name
        self.abbreviation = abbreviation
        self.association = association
        self.division = division
        self.is_women = is_women
        self.members = members

    def add_member(self, member):
        self.members.append(member)
