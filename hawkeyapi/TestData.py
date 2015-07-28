#!/usr/bin/env python

from objects import Season, Team

# TEST DATA!!!!!!!
s1 = Season(
    "NCAA",
    True,
    2013,
    2014,
    ("2013-09-25", "2014-02-23"),
    ("2014-02-28", "2014-03-09"),
    ("2014-03-10", "2014-03-23")
)
s2 = Season(
    "NCAA",
    True,
    2014,
    2015,
    ("2014-10-03", "2015-02-20"),
    ("2015-02-27", "2015-03-08"),
    ("2015-03-13", "2015-03-25")
)
s3 = Season(
    "NCAA",
    True,
    2015,
    2016,
    ("2015-09-24", "2016-02-21"),
    ("2016-02-26", "2016-03-06"),
    ("2016-03-11", "2016-03-20")
)

seasons = [s1, s2, s3]

t1 = Team(
    "Rochester Institute of Technology",
    "Tigers",
    True,
    "College Hockey America",
    {'twitter': '@RITWHKY', 'instagram': '@ritwhky'},
    {'index_url': 'http://ritathletics.com/index.aspx?path=whock', 'data_provider': 'SidearmLegacyProvider'},
)

t2 = Team(
    "Lindenwood University",
    "Lady Lions",
    True,
    "College Hockey America",
    {'twitter': 'LULionsHockey'},
    {'index_url': 'http://www.lindenwoodlions.com/index.aspx?path=whockey', 'data_provider': 'SidearmAdaptiveProvider'},
)

t3 = Team(
    "Penn State University",
    "Nittany Lions",
    True,
    "College Hockey America",
    {'twitter':""},
    {'index_url': 'http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body.html', 'data_provider': 'CBSInteractiveProvider'},
)

t4 = Team(
    "Princeton University",
    "Tigers",
    True,
    "ECAC",
    {'twitter':""},
    {'index_url': 'http://www.goprincetontigers.com/SportSelect.dbml?DB_OEM_ID=10600&KEY=&SPID=4275&SPSID=46915', 'data_provider': 'NeulionClassicProvider'},
)

t5 = Team(
    "Dartmouth University",
    "Big Green",
    True,
    "ECAC",
    {'twitter': ""},
    {'index_url': 'http://www.dartmouthsports.com/SportSelect.dbml?DB_OEM_ID=11600&SPID=4726&SPSID=48905&DB_OEM_ID=11600', 'data_provider': 'NeulionLegacyProvider'},
)

t6 = Team(
    "University of North Dakota",
    None,
    True,
    "WCHA",
    {'twitter': ""},
    {'index_url': 'http://www.undsports.com/SportSelect.dbml?DB_OEM_ID=13500&SPID=6403&SPSID=58668&KEY=', 'data_provider': 'NeulionAdaptiveProvider'},
)

t7 = Team(
    "Harvard University",
    "Crimson",
    True,
    "ECAC",
    None,
    {'index_url': 'http://www.gocrimson.com/sports/wice/index', 'data_provider': 'PrestoSimpleProvider'},
)

t8 = Team(
    "Yale University",
    "Bulldogs",
    True,
    "ECAC",
    None,
    {'index_url': 'http://www.yalebulldogs.com/sports/w-hockey/index', 'data_provider': 'PrestoLegacyProvider'},
)

t9 = Team(
    "Quinnipiac University",
    "Bobcats",
    True,
    "ECAC",
    None,
    {'index_url': 'http://quinnipiacbobcats.com/sports/wice/index', 'data_provider': 'PrestoMonthlyProvider'},
)

t10 = Team(
    "Bemidji State University",
    "Beavers",
    True,
    "WCHA",
    None,
    {'index_url': 'http://www.bsubeavers.com/whockey/', 'data_provider': 'StreamlineProvider'},
)

teams = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
