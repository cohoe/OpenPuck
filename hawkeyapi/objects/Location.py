#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Location(HawkeyApiObject):
    def __init__(self, id, cn, street, city, state, postal, country):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.cn = cn
        self.street = street
        self.city = city
        self.state = state
        self.postal = postal
        self.country = country
