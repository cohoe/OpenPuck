#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 

class Team(HawkeyApiObject):
    def __init__(self, institution, mascot, is_women, home_conference, social_media, website):
        HawkeyApiObject.__init__(self)

        self.institution_name = institution
        self.mascot = mascot
        self.is_women = is_women
        self.home_conference = home_conference
        self.social_media = social_media
        self.website = website
