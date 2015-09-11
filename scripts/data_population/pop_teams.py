#!/usr/bin/env python

from hawkeyapi.models import TeamModel

# RIT, Northeastern, Dartmouth, Princeton, North Dakota, Merrimack, Yale, Maine, Penn State, Bemidji 
rit = TeamModel(
    name = "Rochester Institute of Technology",
    is_women = True,
    mascot = "Tigers",
    home_conference = "CHA",
    league = "NCAA",
    web_site = "http://ritathletics.com/index.aspx?path=whock",
    web_provider = "SidearmLegacyProvider",
)
rit.save()

nu = TeamModel(
    name = "Northeastern University",
    is_women = True,
    mascot = "Huskies",
    home_conference = "WHEA",
    league = "NCAA",
    web_site = "http://www.gonu.com/index.aspx?path=whockey",
    web_provider = "SidearmAdaptiveProvider",
)
nu.save()

du = TeamModel(
    name = "Dartmouth University",
    is_women = True,
    mascot = "Big Green",
    home_conference = "ECAC",
    league = "NCAA",
    web_site = "http://www.dartmouthsports.com/SportSelect.dbml?SPID=4726&SPSID=48905",
    web_provider = "NeulionLegacyProvider",
)
du.save()

pu = TeamModel(
    name = "Princeton University",
    is_women = True,
    mascot = "Tigers",
    home_conference = "ECAC",
    league = "NCAA",
    web_site = "http://www.goprincetontigers.com/SportSelect.dbml?SPID=4275&SPSID=46915",
    web_provider = "NeulionClassicProvider",
)
pu.save()

und = TeamModel(
    name = "University of North Dakota",
    is_women = True,
    mascot = "",
    home_conference = "WCHA",
    league = "NCAA",
    web_site = "http://www.undsports.com/SportSelect.dbml?SPID=6403",
    web_provider = "NeulionAdaptiveProvider",
)
und.save()

mc = TeamModel(
    name = "Merrimack University",
    is_women = True,
    mascot = "Warriors",
    home_conference = "WHEA",
    league = "NCAA",
    web_site = "http://merrimackathletics.com/sports/wice/index",
    web_provider = "PrestoMonthlyProvider",
)
mc.save()

yu = TeamModel(
    name = "Yale University",
    is_women = True,
    mascot = "Bulldogs",
    home_conference = "ECAC",
    league = "NCAA",
    web_site = "http://www.yalebulldogs.com/sports/w-hockey/index",
    web_provider = "PrestoLegacyProvider",
)
yu.save()

ume = TeamModel(
    name = "University of Maine",
    is_women = True,
    mascot = "Black Bears",
    home_conference = "WHEA",
    league = "NCAA",
    web_site = "http://goblackbears.com/sports/w-hockey/index",
    web_provider = "PrestoSimpleProvider",
)
ume.save()

psu = TeamModel(
    name = "Penn State University",
    is_women = True,
    mascot = "Nittany Lions",
    home_conference = "CHA",
    league = "NCAA",
    web_site = "http://www.gopsusports.com/sports/w-hockey/psu-w-hockey-body.html",
    web_provider = "CBSInteractiveProvider",
)
psu.save()

bsu = TeamModel(
    name = "Bemidji State University",
    is_women = True,
    mascot = "Beavers",
    home_conference = "WCHA",
    league = "NCAA",
    web_site = "http://www.bsubeavers.com/whockey/",
    web_provider = "StreamlineProvider",
)
bsu.save()
