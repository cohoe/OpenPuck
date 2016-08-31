#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 
import hawkeyapi.providers

class Team(HawkeyApiObject):
    def __init__(self, id, institution, mascot, is_women, home_conference, social_media, web_site, web_provider, league):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.institution = institution
        self.mascot = mascot
        self.is_women = is_women
        self.home_conference = home_conference
        self.social_media = social_media
        self.website = web_site
        self.provider = web_provider
        self.league = league


    def get_provider(self):
        """
        Return an object of the appropriate provider for a team website.
        """

        if self.provider == "CBSInteractiveProvider":
            return hawkeyapi.providers.CBSInteractiveProvider(self)
        if self.provider == "NeulionAdaptiveProvider":
            return hawkeyapi.providers.NeulionAdaptiveProvider(self)
        if self.provider == "NeulionClassicProvider":
            return hawkeyapi.providers.NeulionClassicProvider(self)
        if self.provider == "NeulionLegacyProvider":
            return hawkeyapi.providers.NeulionLegacyProvider(self)
        if self.provider == "PrestoLegacyProvider":
            return hawkeyapi.providers.PrestoLegacyProvider(self)
        if self.provider == "PrestoMonthlyProvider":
            return hawkeyapi.providers.PrestoMonthlyProvider(self)
        if self.provider == "PrestoSimpleProvider":
            return hawkeyapi.providers.PrestoSimpleProvider(self)
        if self.provider == "SidearmLegacyProvider":
            return hawkeyapi.providers.SidearmLegacyProvider(self)
        if self.provider == "SidearmAdaptiveProvider":
            return hawkeyapi.providers.SidearmAdaptiveProvider(self)
        if self.provider == "SidearmResponsiveProvider":
            return hawkeyapi.providers.SidearmResponsiveProvider(self)
        if self.provider == "StreamlineProvider":
            return hawkeyapi.providers.StreamlineProvider(self)
        else:
            raise Exception("Invalid provider given (%s)" % self.provider)

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__module__, self.id, self.provider)