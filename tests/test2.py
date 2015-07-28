#!/usr/bin/env python

from hawkeyapi.providers import *
from hawkeyapi.objects import ScheduleEntry, Season, Team, Conference, Institution

s = Season(
    2014,
    2015,
    ("2015-09-24", "2016-02-21"),
    ("2016-02-26", "2016-03-06"),
    ("2016-03-11", "2016-03-20")
)

#print s.json()

t = Team(
    "Rochester Institute of Technology",
    "Tigers",
    True,
    "College Hockey America",
    {'twitter': '@RITWHKY', 'instagram': '@ritwhky'},
    {'index_url': 'http://ritathletics.com/index.aspx?path=whock', 'data_provider': 'SidearmLegacyProvider'},
)

#print t.json()

c = Conference(
    'College Hockey America',
    'CHA',
    'NCAA',
    '1',
    True,
    [
        {
            'institution_name': 'Rochester Institute of Technology',
            'member_since': 2012,
        },
        {
            'institution_name': 'Penn State University',
            'member_since': 2012,
        }
    ],
)

#print c.json()

i = Institution(
    'Rochester Institute of Technology',
    'RIT',
    {
        'street_address': '1 Lomb Memorial Drive',
        'city': 'Rochester',
        'state': 'NY',
        'postal_code': 14623,
    }
)

print i.json()
