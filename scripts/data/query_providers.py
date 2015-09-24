#!/usr/bin/env python

from hawkeyapi.database import Teams
from hawkeyapi.factories import TeamFactory

teams = Teams.query_2(
    index='ProviderIndex',
    provider__eq='CBSInteractiveProvider',
    is_women__eq=True,
)

for t in teams:
    team = TeamFactory.objectify(t)
    print team.id
