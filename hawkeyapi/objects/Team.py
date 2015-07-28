#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 
import hawkeyapi.providers

class Team(HawkeyApiObject):
    def __init__(self, institution, mascot, is_women, home_conference, social_media, website):
        HawkeyApiObject.__init__(self)

        self.institution_name = institution
        self.mascot = mascot
        self.is_women = is_women
        self.home_conference = home_conference
        self.social_media = social_media
        self.website = website


    def get_provider(self):
        """
        Return an object of the appropriate provider for a team website.
        """
        provider = self.website['data_provider']

        if provider is "CBSInteractiveProvider":
            return hawkeyapi.providers.CBSInteractiveProvider(self)
        if provider is "NeulionAdaptiveProvider":
            return hawkeyapi.providers.NeulionAdaptiveProvider(self)
        if provider is "NeulionClassicProvider":
            return hawkeyapi.providers.NeulionClassicProvider(self)
        if provider is "NeulionLegacyProvider":
            return hawkeyapi.providers.NeulionLegacyProvider(self)
        if provider is "PrestoLegacyProvider":
            return hawkeyapi.providers.PrestoLegacyProvider(self)
        if provider is "PrestoMonthlyProvider":
            return hawkeyapi.providers.PrestoMonthlyProvider(self)
        if provider is "PrestoSimpleProvider":
            return hawkeyapi.providers.PrestoSimpleProvider(self)
        if provider is "SidearmLegacyProvider":
            return hawkeyapi.providers.SidearmLegacyProvider(self)
        if provider is "SidearmAdaptiveProvider":
            return hawkeyapi.providers.SidearmAdaptiveProvider(self)
        if provider is "StreamlineProvider":
            return hawkeyapi.providers.StreamlineProvider(self)
