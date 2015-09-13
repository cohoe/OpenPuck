#!/usr/bin/env python

from hawkeyapi.database import Seasons

Seasons.put_item(data={
    'league': 'NCAA',
    'id': '2014-15W',
    'is_women': True,
    'start': 2014,
    'end': 2015,
    'confplay': ["2014-10-03", "2015-02-20"],
    'conftour': ["2015-02-27", "2015-03-08"],
    'nattour': ["2015-03-13", "2015-03-25"],
},
overwrite=True)

Seasons.put_item(data={
    'league': 'NCAA',
    'id': '2013-14W',
    'is_women': True,
    'start': 2013,
    'end': 2014,
    'confplay': ["2013-09-25", "2014-02-23"],
    'conftour': ["2014-02-28", "2014-03-09"],
    'nattour': ["2014-03-10", "2014-03-23"],
},
overwrite=True)

Seasons.put_item(data={
    'league': 'NCAA',
    'id': '2015-16W',
    'is_women': True,
    'start': 2015,
    'end': 2016,
    'confplay': ["2015-09-24", "2016-02-21"],
    'conftour': ["2016-02-26", "2016-03-06"],
    'nattour': ["2016-03-11", "2016-03-20"],
},
overwrite=True)

#item = Teams.get_item('NCAA-RIT-W')
#print item['id']
