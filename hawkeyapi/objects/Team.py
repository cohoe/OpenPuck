#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 
import hawkeyapi.providers

class Team(HawkeyApiObject):
    def __init__(self, institution, mascot, is_women, home_conference, social_media, web_site, web_provider):
        HawkeyApiObject.__init__(self)

        self.institution_name = institution
        self.mascot = mascot
        self.is_women = is_women
        self.home_conference = home_conference
        self.social_media = social_media
        self.website = web_site
        self.provider = web_provider


    def get_provider(self):
        """
        Return an object of the appropriate provider for a team website.
        """
        #provider = self.website['data_provider']

        if self.provider is "CBSInteractiveProvider":
            return hawkeyapi.providers.CBSInteractiveProvider(self)
        if self.provider is "NeulionAdaptiveProvider":
            return hawkeyapi.providers.NeulionAdaptiveProvider(self)
        if self.provider is "NeulionClassicProvider":
            return hawkeyapi.providers.NeulionClassicProvider(self)
        if self.provider is "NeulionLegacyProvider":
            return hawkeyapi.providers.NeulionLegacyProvider(self)
        if self.provider is "PrestoLegacyProvider":
            return hawkeyapi.providers.PrestoLegacyProvider(self)
        if self.provider is "PrestoMonthlyProvider":
            return hawkeyapi.providers.PrestoMonthlyProvider(self)
        if self.provider is "PrestoSimpleProvider":
            return hawkeyapi.providers.PrestoSimpleProvider(self)
        if self.provider is "SidearmLegacyProvider":
            return hawkeyapi.providers.SidearmLegacyProvider(self)
        if self.provider is "SidearmAdaptiveProvider":
            return hawkeyapi.providers.SidearmAdaptiveProvider(self)
        if self.provider is "StreamlineProvider":
            return hawkeyapi.providers.StreamlineProvider(self)
