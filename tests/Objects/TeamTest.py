#!/usr/bin/env python

from hawkeyapi.objects import Team
from uuid import uuid4

teamObj = Team(
    id=uuid4(),
    institution='Rochester Institute of Technology',
    mascot='lolcats',
    is_women=True,
    home_conference='LOLZWHATISTHIS',
    social_media='FOOBAR',
    web_site='lolz',
    web_provider='SidearmResponsiveProvider',
    league='LOLZLEAGUE'
)

print teamObj