#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 
import hawkeyapi.providers
from hawkeyapi.providers.util import get_provider_for_url

class Team(HawkeyApiObject):
    def __init__(self, id, institution, mascot, is_women, home_conference, social_media, web_site, league, web_provider=None):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.institution = institution
        self.mascot = mascot
        self.is_women = is_women
        self.home_conference = home_conference
        self.social_media = social_media
        self.website = web_site
        self.league = league

        self.provider = web_provider
        if self.provider is None:
            self.provider = get_provider_for_url(self.website).get_name()


    def get_provider(self, season):
        """
        Return an object of the appropriate provider for a team website.
        """

        if self.provider == "CBSInteractiveProvider":
            return hawkeyapi.providers.CBSInteractiveProvider(self, season)
        if self.provider == "NeulionAdaptiveProvider":
            return hawkeyapi.providers.NeulionAdaptiveProvider(self, season)
        if self.provider == "NeulionClassicProvider":
            return hawkeyapi.providers.NeulionClassicProvider(self, season)
        if self.provider == "NeulionLegacyProvider":
            return hawkeyapi.providers.NeulionLegacyProvider(self, season)
        if self.provider == "PrestoLegacyProvider":
            return hawkeyapi.providers.PrestoLegacyProvider(self, season)
        if self.provider == "PrestoMonthlyProvider":
            return hawkeyapi.providers.PrestoMonthlyProvider(self, season)
        if self.provider == "PrestoSimpleProvider":
            return hawkeyapi.providers.PrestoSimpleProvider(self, season)
        if self.provider == "SidearmLegacyProvider":
            return hawkeyapi.providers.SidearmLegacyProvider(self, season)
        if self.provider == "SidearmAdaptiveProvider":
            return hawkeyapi.providers.SidearmAdaptiveProvider(self, season)
        if self.provider == "SidearmResponsiveProvider":
            return hawkeyapi.providers.SidearmResponsiveProvider(self, season)
        if self.provider == "StreamlineProvider":
            return hawkeyapi.providers.StreamlineProvider(self, season)
        else:
            raise Exception("Invalid provider given (%s)" % self.provider)

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__module__, self.id, self.provider)